# flake8: noqa:E501
# pylint: disable=global-variable-not-assigned
# pylint: disable=broad-exception-caught
# pylint: disable=invalid-name

import logging
import time

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.core.validators import validate_email
from django.utils.timezone import now, timedelta

from core.libs.inbox import InboxMessage
from core.models import (
    MailingBounce,
    MailingBounceManager,
    MailingPoolManager,
    SmtpSender,
)
from core.models.enums import MailingBounceStatus, MailingPoolStatus
from core.models.mailing import MailingProcessingCacheManager, MailingResignationManager
from core.services import BlacklistService, MxService, SenderSmtpService
from core.services.mailing import MailingResignationService

logging.getLogger("flufl.bounce").setLevel(logging.WARNING)


INBOX_SCAN_CACHE = {}

SLEEP_BETWEEN_LOOPS_SECONDS = 10


def process_scan_inbox(smtp_sender: SmtpSender):
    """Scan inboxes process"""
    global INBOX_SCAN_CACHE

    smtp_service = SenderSmtpService(smtp_sender)
    pop3 = smtp_service.get_pop3_instance()
    bounce_manager = MailingBounceManager()

    # Iterate over inbox messages
    for message in smtp_service.get_inbox_messages(pop3):
        _, _, message_bytes = message
        inbox_message = InboxMessage(message_bytes)
        bounces_list = []

        # Skip cached messages
        if INBOX_SCAN_CACHE.get(inbox_message.unique_hash):
            print("# CACHED:", inbox_message.subject_header)
            continue

        print("\n# MESSAGE:", inbox_message.subject_header)

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

        # Save detected failures
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

        # Detect vacation messages and temporarily blacklist emails:
        # - from email
        # - emails in subject
        if inbox_message.is_vacation():
            email = inbox_message.from_email
            print(
                "Is vacation (temporarily blacklisted):",
                inbox_message.subject_header,
            )
            # Temporarily blacklist from email
            BlacklistService.blacklist_email_temporarily(email)
            print(f"- temporarily blacklisted (from email): {email}")
            subject_emails = inbox_message.get_subject_emails()

            # Temporarily blacklist emails contained within subject
            for email in subject_emails:
                BlacklistService.blacklist_email_temporarily(email)
                print(f"- temporarily blacklisted (from subject): {email}")

        # Check if subject is resignation
        # if message is subject resignation then mark from email
        # and all email in the subject as resignations
        if inbox_message.is_subject_resignation():
            resignation_manager = MailingResignationManager()
            from_email = inbox_message.from_email
            print("Resigntion (from e-mail):", from_email)
            resignation_manager.get_or_create_resignation(from_email)
            resignation_manager.mark_confirmed_by_email(from_email)
            subject_emails = inbox_message.get_subject_emails()
            for subject_email in subject_emails:
                print("Resigntion (subject e-mail):", subject_email)
                resignation_manager.get_or_create_resignation(subject_email)
                resignation_manager.mark_confirmed_by_email(subject_email)
            resignation_manager.close()

        # TODO: Detect aggressor
        # TODO: Detect "Please don't spam me"

        # Cache message ID if not already in cache
        if not INBOX_SCAN_CACHE.get(inbox_message.unique_hash):
            print("[*] Adding to cache:", inbox_message.unique_hash)
            # Add to local cache
            INBOX_SCAN_CACHE[inbox_message.unique_hash] = True
            # Add to remote cache
            cache_manager = MailingProcessingCacheManager()
            cache_manager.insert_message_id_into_cache(inbox_message.unique_hash)
            cache_manager.close()

    try:
        pop3.quit()
    except Exception as e:
        print("[-] pop3.quit():", str(e))

    bounce_manager.close()


def process_check_mx(pool_manager: MailingPoolManager, /, *, process_count: int = 100):
    """Check MX process"""

    # MX check process
    pool_being_processed = pool_manager.find_all_by_status(
        MailingPoolStatus.BEING_PROCESSED
    )

    for idx, document in enumerate(pool_being_processed):
        if idx >= process_count:
            break

        campaign_id, email = document["campaign_id"], document["email"]
        document_id = f"{campaign_id}:{email}"

        # Check email format
        try:
            validate_email(email)
        except ValidationError:
            pool_manager.change_status(
                document_id, MailingPoolStatus.INVALID_EMAIL_FORMAT
            )
        else:
            # Check MX status
            new_status = {
                True: MailingPoolStatus.MX_VALID,
                False: MailingPoolStatus.MX_INVALID,
            }[MxService().has_email_mx_record(email)]

            # Change status
            pool_manager.change_status(f"{campaign_id}:{email}", new_status)
            print(idx + 1, email, "->", new_status)


def process_blacklist(pool_manager: MailingPoolManager, /, *, process_count: int = 100):
    """Blacklist process"""

    # Pool blacklist process
    pool_mx_valid = pool_manager.find_all_by_status(MailingPoolStatus.MX_VALID)

    for idx, document in enumerate(pool_mx_valid):
        if idx >= process_count:
            break

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

        elif MailingResignationService.is_email_confirmed_resignation(email):
            new_status = MailingPoolStatus.RESIGNATION

        else:
            new_status = MailingPoolStatus.READY_TO_SEND

        pool_manager.change_status(document_id, new_status)
        print(idx + 1, document_id, "->", new_status)


def process_bounces(
    pool_manager: MailingPoolManager,
    bounce_manager: MailingBounceManager,
    /,
    *,
    process_count: int = 100,
):
    """Blacklist process"""

    # Pool blacklist process
    pool_mx_valid = pool_manager.find_all_by_status(MailingPoolStatus.MX_VALID)

    for idx, document in enumerate(pool_mx_valid):
        if idx >= process_count:
            break
        email = document["email"]
        campaign_id = document["campaign_id"]
        document_id = f"{campaign_id}:{email}"

        bounce = bounce_manager.is_email_bounced(email)

        if not bounce:
            print(f"[*] Not a bounce: `{email}`")
            continue

        new_bounce_type = {
            MailingBounceStatus.PERMANENT: MailingPoolStatus.BOUNCE_PERMANENT,
            MailingBounceStatus.TEMPORARY: MailingPoolStatus.BOUNCE_TEMPORARY,
        }.get(bounce["bounce_type"], MailingPoolStatus.BOUNCE_UNKNOWN)

        pool_manager.change_status(document_id, new_bounce_type)
        print(idx, document_id, "->", new_bounce_type)


def load_cache():
    """Load cache from mongo"""
    global INBOX_SCAN_CACHE

    print("[*] Loading cache ...")

    cache_manager = MailingProcessingCacheManager()

    counter = 0

    for message_id in cache_manager.get_all_cached_message_ids():
        counter += 1
        INBOX_SCAN_CACHE[message_id] = True

    cache_manager.close()

    print(f"[*] Loaded {counter:,} elements from cache")


class Command(BaseCommand):
    """Mailing processing command"""

    help = "Mailing processing"

    def add_arguments(self, parser):
        pass

    def start_loop(self):
        """Start infinite loop"""
        next_inbox_scan_at = now() - timedelta(days=999)

        while True:
            #
            # Open managers
            pool_manager = MailingPoolManager()
            bounce_manager = MailingBounceManager()
            #
            # Run inboxes scan every hour
            if now() > next_inbox_scan_at:
                next_inbox_scan_at = now() + timedelta(hours=1)
                for sender in SmtpSender.objects.all():  # pylint: disable=no-member
                    process_scan_inbox(sender)
            #
            # Run at every loop
            process_check_mx(pool_manager, process_count=200)
            process_bounces(pool_manager, bounce_manager, process_count=100)
            process_blacklist(pool_manager, process_count=100)

            #
            # Close managers
            pool_manager.close()
            bounce_manager.close()

            #
            # Sleep between loops
            print(f"[*] Waiting {SLEEP_BETWEEN_LOOPS_SECONDS} seconds ...")
            time.sleep(SLEEP_BETWEEN_LOOPS_SECONDS)

    def handle(self, *args, **options):
        # Load cache once at the start of program
        load_cache()
        print(f"\n[*] Cache has {len(INBOX_SCAN_CACHE):,} elements")

        # Start infinite loop
        self.start_loop()
