"""
Mailing sending procedure
"""

# flake8: noqa:E501
# pylint: disable=global-variable-not-assigned
# pylint: disable=broad-exception-caught
# pylint: disable=unused-variable
# pylint: disable=invalid-name

import time
import traceback
from smtplib import SMTPRecipientsRefused, SMTPServerDisconnected

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import F
from django.urls import reverse

from core.consts import TelegramChats
from core.libs.mailing.handlers import (
    handle_any_error_occured,
    handle_connection_refused_error,
    handle_daily_sending_limit_reached,
    handle_smtp_recipients_refused_error,
    handle_smtp_server_disconnected_error,
    handle_timeout_error,
    handle_too_much_failures,
    try_to_finish_campaign,
)
from core.models import MailingCampaign, MailingPoolManager, MailingTemplate, SmtpSender
from core.models.enums import MailingPoolStatus
from core.services import SenderSmtpService, TelegramService
from core.services.mailing import MailingResignationService, MailingTrackingService

BASE_URL = settings.BASE_URL

MINUTE = 60
HOUR = 60 * 60


class ProcessSendingStatus:
    """Process sending status"""

    NO_EMAILS_SENT = "NO_EMAILS_SENT"
    LIMIT_REACHED = "LIMIT_REACHED"
    LIMIT_NOT_REACHED = "LIMIT_NOT_REACHED"


def process_sending(campaign_id: int, /, *, limit: int = 100) -> str:
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
    pool_manager = MailingPoolManager()
    documents = pool_manager.get_ready_to_send_for_campaign(campaign_id)

    # Open SMTP connection to sender
    connection = smtp_service.get_smtp_connection()
    return_value: str = ProcessSendingStatus.LIMIT_NOT_REACHED
    send_attempt_counter: int = 0

    for loop_idx, document in enumerate(documents):
        if loop_idx >= limit:
            return_value = ProcessSendingStatus.LIMIT_REACHED
            break

        subject = campaign.get_random_subject()
        email = document["email"]
        document_id = f"{campaign_id}:{email}"
        text_content = text
        html_content = html

        resignation_code = MailingResignationService.get_or_create_inactive_resignation(
            email, campaign.resignation_list
        )
        tracking_code = MailingTrackingService.get_or_create_tracking(email)
        resignation_url = BASE_URL + reverse(
            "core:mailing_resignation_page_with_list",
            kwargs={
                "resignation_code": resignation_code,
                "resignation_list": campaign.resignation_list,
            },
        )

        print("[*] Processing email:", email, resignation_url)

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
            )
        except TimeoutError as exception:
            handle_timeout_error(document_id, pool_manager)
        except SMTPServerDisconnected as exception:
            handle_any_error_occured(campaign_id)
            handle_smtp_server_disconnected_error(
                campaign_id, document_id, pool_manager
            )
        except ConnectionRefusedError as exception:
            handle_any_error_occured(campaign_id)
            handle_connection_refused_error(campaign_id, document_id, pool_manager)
        except SMTPRecipientsRefused as exception:
            handle_any_error_occured(campaign_id)
            handle_smtp_recipients_refused_error(campaign_id, document_id, pool_manager)
        else:
            pool_manager.change_status(document_id, MailingPoolStatus.SENT)
            print(f"[+] Sent to `{email}`")

            # Increment sent counters
            MailingCampaign.manager.filter(id=campaign_id).update(
                stat_sent=F("stat_sent") + 1
            )

            # Increment sent so far counter if limit per day is set
            if campaign.limit_per_day != 0:
                MailingCampaign.manager.filter(id=campaign_id).update(
                    limit_sent_so_far=F("limit_sent_so_far") + 1
                )

    pool_manager.close()  # close mongo manager

    try:
        connection.close()  # close SMTP connection
    except Exception as e:
        pass  # don't care

    if send_attempt_counter == 0:
        return_value = ProcessSendingStatus.NO_EMAILS_SENT

    return return_value


def can_process_campaing(campaign_id: int, mod: int, reminder: int) -> bool:
    """can_process_campaing"""
    return campaign_id % mod == reminder


class Command(BaseCommand):
    """Mailing sending command

    - Send emails from active campaigns

    """

    help = "Mailing sending"

    def add_arguments(self, parser):
        parser.add_argument("mod", type=int)
        parser.add_argument("reminder", type=int)

    def start_loop(self, mod: int, reminder: int):
        """Start infinite loop"""

        while True:
            #
            # Get all active mailing campaigns
            active_campaigns = MailingCampaign.manager.active_campaigns()

            #
            # Sleep and continue loop if no active campaigns
            if active_campaigns.count() == 0:
                print("[*] No active campaigns, sleeping 20s ...")
                time.sleep(20)
                continue

            #
            # Iterate over active campaigns and start sending process
            for campaign in active_campaigns:
                campaign_id: int = campaign.id  # type: ignore

                if not can_process_campaing(campaign_id, mod, reminder):
                    print("[-] Can't process this campaign (not my reminder)")
                    continue

                campaign_id: int = campaign.id  # type: ignore
                print("\n[*] Processing campaign:", campaign)

                # Check if limit per day was reached:
                if campaign.is_daily_sending_limit_reached:
                    handle_daily_sending_limit_reached(campaign)
                # Check if too much failures counted
                elif campaign.failure_counter >= 250:
                    handle_too_much_failures(campaign_id, campaign.title)
                # If everything OK try to send emails batch
                else:
                    print("[*] Processing campaign", campaign_id)
                    result = process_sending(campaign_id, limit=100)
                    # Try to finish campaign
                    if result == ProcessSendingStatus.NO_EMAILS_SENT:
                        print("[*] No email sent with campaign:", campaign)
                        try_to_finish_campaign(campaign_id, campaign.title)

            print("[*] Sleeping 3s between sending ...")
            time.sleep(3)

    def handle(self, *args, **options):
        telegram_service = TelegramService()

        mod: int = options["mod"]
        reminder: int = options["reminder"]

        # Infinite loop
        while True:

            # Retry loop
            retry = 0
            while retry <= 5:
                try:
                    self.start_loop(mod, reminder)
                except Exception as e:
                    retry += 1
                    formatted_lines = "\n".join(traceback.format_exc().splitlines())
                    telegram_service.try_send_chat_message(
                        f"retry={retry}, {e}:\n{formatted_lines}",
                        TelegramChats.OTHER,
                    )
                    print("[*] Waiting after failure")
                    time.sleep(retry * (3 * MINUTE))
                else:
                    retry = 0

            # When something went completely wrong send telegram message
            telegram_service.try_send_chat_message(
                "MAILING PROCESSING KOMPLETNIE SIĘ WYJEBAŁ",
                TelegramChats.OTHER,
            )
            print("Complete failure")
            time.sleep(HOUR)
