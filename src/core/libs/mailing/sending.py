"""Mailing Sending"""

# flake8: noqa:E501
# pylint: disable=global-variable-not-assigned
# pylint: disable=broad-exception-caught
# pylint: disable=unused-variable
# pylint: disable=invalid-name

import time
from smtplib import SMTPRecipientsRefused, SMTPServerDisconnected

from django.conf import settings
from django.db.models import F
from django.urls import reverse

from core.libs.mailing.handlers import (
    handle_any_error_occured,
    handle_connection_refused_error,
    handle_smtp_recipients_refused_error,
    handle_smtp_server_disconnected_error,
    handle_timeout_error,
)
from core.libs.mailing.title_test import get_or_create_mailing_title_test
from core.models import (
    MailingCampaign,
    MailingPoolManager,
    MailingTemplate,
    MailingTitleTest,
    SmtpSender,
)
from core.models.enums import MailingPoolStatus
from core.services import SenderSmtpService
from core.services.mailing import MailingResignationService, MailingTrackingService

BASE_URL = settings.BASE_URL


def process_sending(
    pool_manager: MailingPoolManager,
    campaign_id: int,
    bucket_id: int,
    /,
    *,
    limit: int = 100,
):
    """Mailing sending process"""

    # Get campaign
    campaign: MailingCampaign = MailingCampaign.manager.get(id=campaign_id)
    alias = campaign.alias

    # Get template
    template: MailingTemplate = campaign.template
    html = template.html
    text = template.text

    # Get SMTP sender account + service
    smtp_sender: SmtpSender = campaign.smtp_sender
    smtp_service = SenderSmtpService(smtp_sender)

    # Open pool manager and get ready to send messages
    documents = [
        doc
        for doc in pool_manager.get_ready_to_send_for_campaign(
            campaign_id, bucket_id, limit=100
        )
    ]

    if len(documents) == 0:
        print(f"[*] No items in pool for bucket_id={bucket_id} -> exiting")
        return 0

    # Open SMTP connection to sender
    print("[+] Opened SMTP connection")
    connection = smtp_service.get_smtp_connection()

    # Define variables
    send_attempt_counter: int = 0

    for loop_idx, document in enumerate(documents):

        # Break on limit reached
        if loop_idx >= limit:
            break

        # Prepare variables
        subject = campaign.get_random_subject()
        email = document["email"]
        document_id = f"{campaign_id}:{email}"
        text_content = text
        html_content = html
        any_error_occured = False

        # Save test a/b subject
        test_title = get_or_create_mailing_title_test(subject, str(campaign_id))
        test_title_id: int = test_title.id  # type: ignore
        # Increment total sent
        MailingTitleTest.objects.filter(id=test_title_id).update(
            total_sent=F("total_sent") + 1
        )

        # Tracking code, get or create
        start_time = time.time()
        tracking_code = MailingTrackingService.get_or_create_tracking(email)
        end_time = time.time()
        time_get_or_create_tracking = (end_time - start_time) * 1000

        # Resignation, get or create
        start_time = time.time()
        resignation_code = MailingResignationService.get_or_create_inactive_resignation(
            email, campaign.resignation_list
        )
        end_time = time.time()
        time_get_or_create_inactive_resignation = (end_time - start_time) * 1000

        # Create resignation URL
        resignation_url = BASE_URL + reverse(
            "core:mailing_resignation_page_with_list",
            kwargs={
                "resignation_code": resignation_code,
                "resignation_list": campaign.resignation_list,
            },
        )

        print(
            f"\n[{loop_idx} / max {limit}] Email: {email}",
            "(resignation: {resignation_code})",
        )
        print(f"Campaign (ID={campaign_id})", campaign.title)
        print("Bucket_id :=", bucket_id)
        print(f"> Tracking: {time_get_or_create_tracking:.2f} ms")
        print(f"> Resignation: {time_get_or_create_inactive_resignation:.2f} ms")

        print(f"Sleeping {campaign.sleep_every_send}s")
        time.sleep(campaign.sleep_every_send)

        try:
            send_attempt_counter += 1
            start_time = time.time()
            smtp_service.send_email(
                connection=connection,
                email=email,
                alias=alias,
                subject=subject,
                html=html_content,
                text=text_content,
                resignation_url=resignation_url,
                tracking_code=tracking_code,
                campaign_id=campaign_id,
                test_subject_id=str(test_title.id),  # type: ignore
            )
            end_time = time.time()
            time_send = (end_time - start_time) * 1000
            print(f"> Send time: {time_send:.2f} ms")
        except TimeoutError as exception:
            handle_timeout_error(document_id, pool_manager)
            print(f"[-] TimeoutError `{email}`: {exception}")
            any_error_occured = True
        except SMTPServerDisconnected as exception:
            handle_any_error_occured(campaign_id)
            handle_smtp_server_disconnected_error(
                campaign_id, document_id, pool_manager
            )
            print(f"[-] SMTPServerDisconnected `{email}`: {exception}")
            any_error_occured = True
        except ConnectionRefusedError as exception:
            handle_any_error_occured(campaign_id)
            handle_connection_refused_error(campaign_id, document_id, pool_manager)
            print(f"[-] ConnectionRefusedError `{email}`: {exception}")
            any_error_occured = True
        except SMTPRecipientsRefused as exception:
            handle_any_error_occured(campaign_id)
            handle_smtp_recipients_refused_error(campaign_id, document_id, pool_manager)
            print(f"[-] SMTPRecipientsRefused `{email}`: {exception}")
            any_error_occured = True
        else:
            pool_manager.change_status(document_id, MailingPoolStatus.SENT)
            print(f"[+] SUCCESSFULLY sent to: `{email}`")

            # Increment daily counters
            pool_manager.inc_todays_sent_counter_for_campaign(campaign_id)
            pool_manager.inc_todays_sent_counter_for_sender(smtp_sender.username)

            pool_manager.inc_hourly_sent_counter_for_campaign(campaign_id)
            pool_manager.inc_hourly_sent_counter_for_sender(smtp_sender.username)

            # Increment sent counters
            MailingCampaign.manager.filter(id=campaign_id).update(
                stat_sent=F("stat_sent") + 1
            )

            # Increment sent so far counter if limit per day is set
            if campaign.limit_per_day != 0:
                MailingCampaign.manager.filter(id=campaign_id).update(
                    limit_sent_so_far=F("limit_sent_so_far") + 1
                )

        # Increment loop sleep if any error occured
        if any_error_occured:
            print("[-] Any error occured, waiting 10 seconds ...")
            time.sleep(10)

            # Refresh smtp connection
            print("[*] Re-establishing SMTP connection...")
            connection = smtp_service.get_smtp_connection()

    try:
        print("[+] Trying to close connection")
        connection.close()  # close SMTP connection
    except Exception as e:
        print("- Exception while closing:", str(e))
    else:
        print("- Closed gracefully")
