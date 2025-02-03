"""Mailing processes"""

# flake8: noqa=E501
# pylint: disable=broad-exception-caught

import time

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from core.consts import TelegramChats
from core.libs.inbox import InboxMessage
from core.models import (
    MailingBounce,
    MailingBounceManager,
    MailingPoolManager,
    MailingReplyMessage,
    SmtpSender,
)
from core.models.enums import MailingBounceStatus, MailingPoolStatus
from core.models.mailing import (
    MailingCampaign,
    MailingProcessingCacheManager,
    MailingResignationManager,
)
from core.services import (
    BlacklistService,
    MxService,
    SenderSmtpService,
    TelegramService,
)
from core.services.mailing import MailingResignationService


def process_scan_inbox(smtp_sender: SmtpSender, cache: dict):
    """Scan inboxes process"""

    smtp_service = SenderSmtpService(smtp_sender)
    pop3 = smtp_service.get_pop3_instance()
    bounce_manager = MailingBounceManager()
    cache_manager = MailingProcessingCacheManager()

    # Iterate over inbox messages
    for message in smtp_service.get_inbox_messages(pop3):
        _, _, message_bytes = message
        inbox_message = InboxMessage(message_bytes)
        bounces_list = []

        print("\n# MESSAGE:", inbox_message.subject_header)

        # Skip cached messages
        if cache.get(inbox_message.unique_hash):
            print("# CACHED:", inbox_message.subject_header)
            continue
        else:
            # Cache message ID if not already in cache
            print("[*] Adding to cache:", inbox_message.unique_hash)
            # Add to local cache
            cache[inbox_message.unique_hash] = True
            # Add to remote cache
            cache_manager.insert_message_id_into_cache(inbox_message.unique_hash)

        # Detect permanent failures
        permanent_failures = inbox_message.get_emails_permanent_failure()
        for email in permanent_failures:
            print("Permanent failure:", email)
            bounces_list.append(
                (
                    email,
                    MailingBounceStatus.PERMANENT,
                    inbox_message.get_content(),
                )
            )

        # Detect temporary failures
        temporary_failures = inbox_message.get_emails_temporary_failure()
        for email in temporary_failures:
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
            print(
                "Is vacation (temporarily blacklisted):",
                inbox_message.subject_header,
            )
            from_email = inbox_message.from_email
            subject_emails = inbox_message.get_subject_emails()
            for tb_email in [from_email, *subject_emails]:
                BlacklistService.blacklist_email_temporarily(tb_email)
                print(f"- temporarily blacklisted: {tb_email}")

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

        # Temporarly ban e-mails from aggressor detected message
        if inbox_message.is_aggressor():
            from_email = inbox_message.from_email
            subject_emails = inbox_message.get_subject_emails()
            for tb_email in [from_email, *subject_emails]:
                BlacklistService.blacklist_email_temporarily(tb_email, days=14)

            which_phrases = inbox_message.which_aggressor_phrases()

            telegram_service = TelegramService()
            telegram_service.try_send_chat_message(
                "\n".join(
                    [
                        "[AGGRESSOR DETECTION] Tymczasowo (14 dni) zablokowano:",
                        " ".join([from_email, *subject_emails]),
                        "\nPonieważ wykryto:",
                        " ".join(which_phrases),
                    ]
                ),
                TelegramChats.OTHER,
            )

        # Save message from inbox into database if
        # 1. doesn't already exists
        # 2. there are no bounces
        # 3. is not bounce by subject
        if all(
            [
                not MailingReplyMessage.manager.filter(
                    email_id=inbox_message.unique_hash
                ).exists(),
                len(permanent_failures) == 0,
                len(temporary_failures) == 0,
                not inbox_message.is_bounce_by_subject(),
            ]
        ):
            print("MailingReplyMessage:", inbox_message.subject_header)
            MailingReplyMessage(
                email_id=inbox_message.unique_hash,
                from_email=inbox_message.from_email,
                to_email=inbox_message.from_email,
                is_aggressor=inbox_message.is_aggressor(),
                is_vacation=inbox_message.is_vacation(),
                is_email_change=inbox_message.is_new_email(),
                subject=inbox_message.subject_header,
                message_content=inbox_message.get_content(),
            ).save()

    try:
        pop3.quit()
    except Exception as e:
        print("[-] pop3.quit():", str(e))

    bounce_manager.close()
    cache_manager.close()


def process_check_mx(
    pool_manager: MailingPoolManager,
    campaigns_ids: list[int],
    /,
    *,
    process_count: int = 100,
):
    """Check MX process"""

    # MX check process
    pool_being_processed = pool_manager.find_all_by_status_and_campaign_ids(
        MailingPoolStatus.BEING_PROCESSED, campaigns_ids
    )  # TODO: OPTYMALIZACJA to bierze całe? jaki index?

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
            time.sleep(0.12)
            # Check MX status
            new_status = {
                True: MailingPoolStatus.MX_VALID,
                False: MailingPoolStatus.MX_INVALID,
            }[MxService().has_email_mx_record(email)]

            # Change status
            pool_manager.change_status(f"{campaign_id}:{email}", new_status)
            print(idx + 1, email, "->", new_status)


def process_blacklist(
    pool_manager: MailingPoolManager,
    campaigns_ids: list[int],
    /,
    *,
    process_count: int = 100,
):
    """Blacklist process"""

    # Pool blacklist process
    pool_mx_valid = pool_manager.find_all_by_status_and_campaign_ids(
        MailingPoolStatus.MX_VALID, campaigns_ids
    )

    for idx, document in enumerate(pool_mx_valid):
        if idx >= process_count:
            break

        email = document["email"]
        campaign_id = document["campaign_id"]
        campaign: MailingCampaign = MailingCampaign.manager.get(id=campaign_id)

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

        elif MailingResignationService.is_email_confirmed_resignation(
            email, campaign.resignation_list
        ):
            new_status = MailingPoolStatus.RESIGNATION

        else:
            new_status = MailingPoolStatus.READY_TO_SEND

        pool_manager.change_status(document_id, new_status)
        print(idx + 1, document_id, "->", new_status)


def process_bounces(
    pool_manager: MailingPoolManager,
    bounce_manager: MailingBounceManager,
    campaigns_ids: list[int],
    /,
    *,
    process_count: int = 100,
):
    """Blacklist process"""

    # Pool blacklist process
    pool_mx_valid = pool_manager.find_all_by_status_and_campaign_ids(
        MailingPoolStatus.MX_VALID, campaigns_ids
    )

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


def process_load_cache():
    """Load cache from mongo"""

    print("[*] Loading cache ...")

    cache = {}
    cache_manager = MailingProcessingCacheManager()

    counter = 0

    for message_id in cache_manager.get_all_cached_message_ids():
        counter += 1
        cache[message_id] = True

    cache_manager.close()

    print(f"[*] Loaded {counter:,} elements from cache")
    return cache
