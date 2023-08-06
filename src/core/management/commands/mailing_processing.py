import logging
import time

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.core.validators import validate_email

from core.libs.inbox import InboxMessage
from core.models import (
    MailingBounce,
    MailingBounceManager,
    MailingPoolManager,
    SmtpSender,
)
from core.models.enums import MailingBounceStatus, MailingPoolStatus
from core.services import BlacklistService, MxService, SenderSmtpService

logging.getLogger("flufl.bounce").setLevel(logging.WARNING)


# TODO: Backoff time/sleep when there is no emails. max 5 minutes
# TODO: Cache for inbox scan


def process_scan_inboxes():
    """Scan inboxes process"""

    # Get all senders
    smtp_senders = SmtpSender.objects.all()

    # Inbox scan process
    for smtp_sender in smtp_senders:
        smtp_service = SenderSmtpService(smtp_sender)
        pop3 = smtp_service.get_pop3_instance()
        bounce_manager = MailingBounceManager()

        for message in smtp_service.get_inbox_messages(pop3):
            _, _, message_bytes = message
            inbox_message = InboxMessage(message_bytes)
            print("\n# MESSAGE:", inbox_message.subject_header)
            bounces_list = []

            # Detect permanent failures
            for email in inbox_message.get_emails_permanent_failure():
                print("Permanent failure:", email)
                bounces_list.append(
                    (
                        email,
                        MailingBounceStatus.PERMANENT,
                        inbox_message.get_content(),
                    )
                )

            # Detect temporary failures
            for email in inbox_message.get_emails_temporary_failure():
                print("Temporary failure:", email)
                bounces_list.append(
                    (
                        email,
                        MailingBounceStatus.PERMANENT,
                        inbox_message.get_content(),
                    )
                )

            # Save bounces
            bounce_manager.upsert_documents(
                [
                    MailingBounce(
                        id=inbox_message.unique_hash,
                        email=email,
                        bounce_type=bounce_type,
                        content=content,
                    )
                    for email, bounce_type, content in bounces_list
                ]
            )

            # Detect vacation messages
            if inbox_message.is_vacation():
                email = inbox_message.from_email
                print("Is vacation:", email, "/", inbox_message.subject_header)
                BlacklistService.blacklist_email_temporarily(email)

            if inbox_message.is_resignation():  # TODO
                email = inbox_message.from_email
                print("Resignation:", email)

        pop3.quit()
        bounce_manager.close()


def process_check_mx(process_count: int):
    """Check MX process"""

    # MX check process
    pool_manager = MailingPoolManager()
    pool_being_processed = pool_manager.find_all_by_status(
        MailingPoolStatus.BEING_PROCESSED
    )

    counter = 0
    for document in pool_being_processed:
        if counter >= process_count:
            break
        counter += 1
        campaign_id, email = document["campaign_id"], document["email"]
        document_id = f"{campaign_id}:{email}"

        # Check email format
        try:
            validate_email(email)
        except ValidationError:
            pool_manager.change_status(
                document_id, MailingPoolStatus.INVALID_EMAIL_FORMAT
            )
            continue

        # Check MX status
        if MxService().has_email_mx_record(email):
            new_status = MailingPoolStatus.MX_VALID
        else:
            new_status = MailingPoolStatus.MX_INVALID

        # Change status
        pool_manager.change_status(f"{campaign_id}:{email}", new_status)
        print(counter, email, "->", new_status)

    pool_manager.close()


def process_blacklist(process_count: int):
    """Blacklist process"""

    # Pool blacklist process
    pool_manager = MailingPoolManager()
    bounce_manager = MailingBounceManager()
    pool_mx_valid = pool_manager.find_all_by_status(MailingPoolStatus.MX_VALID)

    counter = 0
    for document in pool_mx_valid:
        if counter >= process_count:
            break
        counter += 1
        email = document["email"]
        campaign_id = document["campaign_id"]
        document_id = f"{campaign_id}:{email}"
        prefix, domain = email.split("@")

        # Blacklist
        if BlacklistService.is_email_dangerous_to_send(email):
            new_status = MailingPoolStatus.DANGEROUS_TO_SEND

        elif BlacklistService.is_domain_blacklisted(domain):
            new_status = MailingPoolStatus.BLACKLISTED_DOMAIN

        elif BlacklistService.is_email_blacklisted(email):
            new_status = MailingPoolStatus.BLACKLISTED_EMAIL

        elif BlacklistService.is_prefix_blacklisted(prefix):
            new_status = MailingPoolStatus.BLACKLISTED_PREFIX

        elif BlacklistService.is_email_temporarily_blacklisted(email):
            new_status = MailingPoolStatus.BLACKLISTED_EMAIL_TEMPORARY

        elif BlacklistService.is_email_phrase_blacklisted(email):
            new_status = MailingPoolStatus.BLACKLISTED_PHRASE
        else:
            new_status = MailingPoolStatus.READY_TO_SEND

        pool_manager.change_status(document_id, new_status)
        print(counter, document_id, "->", new_status)

    pool_manager.close()
    bounce_manager.close()


def process_bounces(process_count: int):
    """Blacklist process"""

    # Pool blacklist process
    pool_manager = MailingPoolManager()
    bounce_manager = MailingBounceManager()
    pool_mx_valid = pool_manager.find_all_by_status(MailingPoolStatus.MX_VALID)

    counter = 0
    for document in pool_mx_valid:
        if counter >= process_count:
            break
        counter += 1
        email = document["email"]
        campaign_id = document["campaign_id"]
        document_id = f"{campaign_id}:{email}"

        bounce = bounce_manager.is_email_bounced(email)
        if not bounce:
            print(email, "was not a bounce")
            continue
        else:
            bounce_type = bounce["bounce_type"]

        if bounce_type == MailingBounceStatus.PERMANENT:
            new_bounce_type = MailingPoolStatus.BOUNCE_PERMANENT
        elif bounce_type == MailingBounceStatus.TEMPORARY:
            new_bounce_type = MailingPoolStatus.BOUNCE_TEMPORARY
        else:
            new_bounce_type = MailingPoolStatus.BOUNCE_UNKNOWN

        pool_manager.change_status(document_id, new_bounce_type)
        print(counter, document_id, "->", new_bounce_type)

    pool_manager.close()
    bounce_manager.close()


class Command(BaseCommand):
    """Mailing processing command

    - Verify MX
    - Check blacklists
    - Check bounces

    """

    help = "Mailing processing"

    def add_arguments(self, parser):
        pass

    def start_loop(self):
        """Start infinite loop"""
        loop_counter = 0
        while True:
            process_scan_inboxes()
            process_check_mx(200)
            process_bounces(100)
            process_blacklist(100)

            loop_counter += 1
            print("waiting 5 seconds ...")
            time.sleep(5)

    def handle(self, *args, **options):
        self.start_loop()
