"""Mailing processes"""

# flake8: noqa=E501
# pylint: disable=broad-exception-caught

import time
import traceback
from email.message import Message

import mailparser
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Q
from django.utils.timezone import now, timedelta
from mailparser import MailParser

from core.libs.mongo.db import get_mongo_connection
from core.models import (
    MailingBounceManager,
    MailingPoolManager,
    MailingReplyMessage,
    SmtpSender,
    Webinar,
    WebinarParticipant,
)
from core.models.enums import MailingBounceStatus, MailingPoolStatus
from core.models.mailing import MailingCampaign, MailingProcessingCacheManager
from core.services import BlacklistService, MxService, SenderSmtpService
from core.services.mailing import MailingResignationService

from .scan_inbox.aggressor import aggressor_action, aggressor_notify, is_email_aggressor
from .scan_inbox.bounces import (
    get_emails_permanent_failures,
    get_emails_temporary_failures,
    is_bounce_by_subject,
)
from .scan_inbox.new_email import is_new_email
from .scan_inbox.vacation import (
    is_email_content_vacation,
    is_email_subject_vacation,
    vacation_action,
    vacation_notify,
)


def process_inbox_message(smtp_sender: SmtpSender, email_parser: MailParser):
    """process_inbox_message"""

    if isinstance(email_parser.message_id, list):
        message_id = "-".join(email_parser.message_id)
    else:
        message_id = email_parser.message_id

    email_from = email_parser.from_[0][1]
    email_to = email_parser.to[0][1]
    email_text = " ".join(email_parser.text_plain)
    email_subject: str = email_parser.subject  # type: ignore
    message: Message = email_parser.message  # type: ignore

    bounce_manager = MailingBounceManager()

    # Aggressor detection
    is_aggressor = is_email_aggressor(email_subject, email_text)
    if is_aggressor:
        blocked_emails, phrases_context_list = aggressor_action(
            email_from, email_subject, email_text
        )
        print(f">\n>>>>> AGGRESSOR DETECTED: {blocked_emails}\n>")
        aggressor_notify(blocked_emails, phrases_context_list)

    # Detect vacation indicator
    is_vacation_subject = is_email_subject_vacation(email_subject)
    is_vacation_content = is_email_content_vacation(email_text)
    if is_vacation_subject or is_vacation_content:
        print(f">\n>>>>> VACATION DETECTED: {email_from}\n>")
        blocked_emails, phrases_context_list = vacation_action(
            email_from, email_subject, email_text
        )
        vacation_notify(
            email_subject,
            blocked_emails,
            phrases_context_list,
            is_vacation_subject,
            is_vacation_content,
        )

    # Detect permanent failures
    permanent_failures = get_emails_permanent_failures(message)
    for email in permanent_failures:
        print(f">\n>>>>> PERMANENT FAILURE: {email}\n>")
        bounce_manager.upsert_bounce(
            message_id, smtp_sender.username, email, MailingBounceStatus.PERMANENT
        )

    # Detect temporary failures
    temporary_failures = get_emails_temporary_failures(message)
    for email in temporary_failures:
        print(f">\n>>>>> TEMPORARY FAILURE: {email}\n>")
        bounce_manager.upsert_bounce(
            message_id, smtp_sender.username, email, MailingBounceStatus.TEMPORARY
        )

    bounce_manager.close()

    if all(
        [
            not MailingReplyMessage.manager.filter(email_id=message_id).exists(),
            not permanent_failures,
            not temporary_failures,
            not is_bounce_by_subject(email_subject),
        ]
    ):
        MailingReplyMessage(
            email_id=message_id,
            from_email=email_from,
            to_email=email_parser.to,
            is_aggressor=is_aggressor,
            is_vacation=is_vacation_content or is_vacation_subject,
            is_email_change=is_new_email(email_subject, email_text),
            subject=email_subject,
            message_content=" ".join(email_parser.text_html),
        ).save()


def process_scan_inbox(smtp_sender: SmtpSender):
    """process_scan_inbox2"""

    smtp_service = SenderSmtpService(smtp_sender)
    pop3 = smtp_service.get_pop3_instance()
    cache_manager = MailingProcessingCacheManager()

    # Load cache
    cache = process_load_cache()

    # Iterate over inbox messages
    for message in smtp_service.get_inbox_messages(pop3):
        _, _, message_bytes = message

        email_parser = mailparser.parse_from_bytes(message_bytes)

        if isinstance(email_parser.message_id, list):
            message_id = "-".join(email_parser.message_id)
        else:
            message_id = email_parser.message_id

        # Skip cached messages
        if settings.APP_ENV == "production":
            if cache.get(message_id):
                print(">>>>> ALREADY CACHED:", email_parser.subject)
                continue
            else:
                print("[*] Adding to cache:", message_id)
                cache_manager.insert_message_id_into_cache(message_id)  # type: ignore

        print("\n# MESSAGE:", message_id)
        process_inbox_message(smtp_sender, email_parser)

    cache_manager.close()

    try:
        pop3.quit()
    except Exception as e:
        print("[-] pop3.quit():", str(e))


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
        MailingPoolStatus.AWAITING_MX_CHECK, campaigns_ids
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
            time.sleep(0.12)
            # Check MX status
            new_status = {
                True: MailingPoolStatus.READY_TO_SEND,
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
        MailingPoolStatus.AWAITING_BLACKLIST_CHECK, campaigns_ids
    )

    # Aggragete customers
    aggregate_customers: dict[str, list] = {}

    for idx, document in enumerate(pool_mx_valid):
        if idx >= process_count:
            break

        email = document["email"]
        campaign_id = document["campaign_id"]
        campaign: MailingCampaign = MailingCampaign.manager.get(id=campaign_id)

        document_id = f"{campaign_id}:{email}"

        try:
            prefix, domain = email.split("@")
        except Exception as e:
            pool_manager.change_status(
                document_id, MailingPoolStatus.INVALID_EMAIL_FORMAT
            )
            continue

        # If webinar exclude already singed up customers
        if campaign.webinar:
            # Get grouping token
            grouping_token: str = campaign.webinar.grouping_token
            print("[DEBUG] if campaign.webinar, grouping_token:", grouping_token)
            # If not fetched, create a key
            if aggregate_customers.get(grouping_token) is None:
                aggregate_customers[grouping_token] = []
                print("[DEBUG] if not aggregate_customers.get(grouping_token):")
                aggregate_webinars = Webinar.manager.filter(
                    Q(grouping_token=grouping_token)
                    & Q(date__gte=now() - timedelta(days=30))
                )
                for aggregate_webinar in aggregate_webinars:
                    print("[DEBUG] aggregate_webinar", aggregate_webinar)
                    for (
                        participant
                    ) in WebinarParticipant.manager.get_valid_participants_for_webinar(
                        aggregate_webinar
                    ):
                        aggregate_customers[grouping_token].append(
                            participant.email.lower()
                        )

                    print(
                        "[DEBUG] aggregate_customers:",
                        aggregate_customers[grouping_token],
                    )

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
        elif campaign.webinar and email.lower() in aggregate_customers.get(
            campaign.webinar.grouping_token, []
        ):
            new_status = MailingPoolStatus.IS_ALREADY_CUSTOMER
        else:
            new_status = MailingPoolStatus.AWAITING_MX_CHECK

        pool_manager.change_status(document_id, new_status)
        print(idx + 1, document_id, "->", new_status)


def process_anomail(
    pool_manager: MailingPoolManager,
    campaigns_ids: list[int],
    /,
    *,
    process_count: int = 100,
):
    """Process anomail"""

    pool_mx_valid = pool_manager.find_all_by_status_and_campaign_ids(
        MailingPoolStatus.BEING_PROCESSED, campaigns_ids
    )
    for idx, document in enumerate(pool_mx_valid):
        if idx >= process_count:
            break
        email = document["email"]

        if "wykladowca.pl" in email:
            pool_manager.change_status(document_id, MailingPoolStatus.READY_TO_SEND)
            continue

        campaign_id = document["campaign_id"]
        document_id = f"{campaign_id}:{email}"

        campaign: MailingCampaign = MailingCampaign.manager.get(id=campaign_id)

        client, database = get_mongo_connection()

        # Anomail - Bomba
        if campaign.filter_bomba and database.wykladowcav2_anomail_bomba.find_one(
            {"_id": email}
        ):
            pool_manager.change_status(document_id, MailingPoolStatus.ANOMAIL_BOMB)
            print(idx, document_id, "->", MailingPoolStatus.ANOMAIL_BOMB)
            continue

        # Anomail - Miedzynarodowe
        if (
            campaign.filter_miedzynarodowe
            and database.wykladowcav2_anomail_miedzynarodowe.find_one({"_id": email})
        ):
            pool_manager.change_status(
                document_id, MailingPoolStatus.ANOMAIL_MIEDZYNARODOWE
            )
            print(idx, document_id, "->", MailingPoolStatus.ANOMAIL_MIEDZYNARODOWE)
            continue

        # Anomail - Ryzykowne
        if (
            campaign.filter_ryzykowne
            and database.wykladowcav2_anomail_ryzykowne.find_one({"_id": email})
        ):
            pool_manager.change_status(document_id, MailingPoolStatus.ANOMAIL_RYZYKOWNE)
            print(idx, document_id, "->", MailingPoolStatus.ANOMAIL_RYZYKOWNE)
            continue

        print("OK", idx, document_id, "->", MailingPoolStatus.AWAITING_BOUNCE_CHECK)
        pool_manager.change_status(document_id, MailingPoolStatus.AWAITING_BOUNCE_CHECK)

        client.close()


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
        MailingPoolStatus.AWAITING_BOUNCE_CHECK, campaigns_ids
    )

    for idx, document in enumerate(pool_mx_valid):
        if idx >= process_count:
            break
        email = document["email"]
        campaign_id = document["campaign_id"]
        document_id = f"{campaign_id}:{email}"

        campaign: MailingCampaign = MailingCampaign.manager.get(id=campaign_id)
        sender_email = campaign.smtp_sender.username

        bounce = bounce_manager.is_email_bounced_for_sender(sender_email, email)

        if not bounce:
            pool_manager.change_status(
                document_id, MailingPoolStatus.AWAITING_BLACKLIST_CHECK
            )
            print(f"[*] Not a bounce: `{email}`")
            continue

        new_bounce_type = {
            MailingBounceStatus.PERMANENT: MailingPoolStatus.BOUNCE_PERMANENT,
            MailingBounceStatus.TEMPORARY: MailingPoolStatus.BOUNCE_TEMPORARY,
            MailingBounceStatus.SPAMBLOCK: MailingBounceStatus.SPAMBLOCK,
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
