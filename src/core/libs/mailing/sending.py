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
from core.models import MailingCampaign, MailingPoolManager, MailingTemplate, SmtpSender
from core.models.enums import MailingPoolStatus
from core.models.enums.mailing_enums import ProcessSendingStatus
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
) -> str:
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
    documents = pool_manager.get_ready_to_send_for_campaign(campaign_id, bucket_id)

    # Open SMTP connection to sender
    connection = smtp_service.get_smtp_connection()
    return_value: str = ProcessSendingStatus.LIMIT_NOT_REACHED
    send_attempt_counter: int = 0
    sleep_between_each_send = 0

    for loop_idx, document in enumerate(documents):
        # Break on limit reached
        if loop_idx >= limit:
            return_value = ProcessSendingStatus.LIMIT_REACHED
            break

        # Prepare variables
        subject = campaign.get_random_subject()
        email = document["email"]
        document_id = f"{campaign_id}:{email}"
        text_content = text
        html_content = html
        any_error_occured = False

        # Prepare codes and urls
        tracking_code = MailingTrackingService.get_or_create_tracking(email)
        resignation_code = MailingResignationService.get_or_create_inactive_resignation(
            email, campaign.resignation_list
        )
        resignation_url = BASE_URL + reverse(
            "core:mailing_resignation_page_with_list",
            kwargs={
                "resignation_code": resignation_code,
                "resignation_list": campaign.resignation_list,
            },
        )

        print(f"\n[*] Processing email: {email} (resignation: {resignation_code})")

        if sleep_between_each_send:
            print(f"sleep_between_each_send: {sleep_between_each_send}")
            time.sleep(sleep_between_each_send)

        try:
            send_attempt_counter += 1
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
            )
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
            print("[-] Any error occured, waiting 60 seconds ...")
            time.sleep(60)
            sleep_between_each_send = min(0.5, sleep_between_each_send + 0.01)

    try:
        connection.close()  # close SMTP connection
    except Exception as e:
        pass  # don't care

    if send_attempt_counter == 0:
        return_value = ProcessSendingStatus.NO_EMAILS_SENT

    return return_value
