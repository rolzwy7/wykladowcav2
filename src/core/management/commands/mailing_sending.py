"""
Mailing sending procedure
"""

# flake8: noqa:E501
# pylint: disable=line-too-long

import time
from smtplib import SMTPRecipientsRefused, SMTPServerDisconnected

from django.core.management.base import BaseCommand
from django.db.models import F, Q
from django.utils.timezone import now, timedelta

from core.consts import TelegramChats
from core.models import MailingCampaign, MailingPoolManager, MailingTemplate, SmtpSender
from core.models.enums import MailingCampaignStatus, MailingPoolStatus
from core.services import SenderSmtpService, TelegramService


class ProcessSendingStatus:
    """Process sending status"""

    NO_EMAILS_SENT = "NO_EMAILS_SENT"
    LIMIT_REACHED = "LIMIT_REACHED"
    LIMIT_NOT_REACHED = "LIMIT_NOT_REACHED"


def process_sending(campaign_id: int, /, *, limit: int = 100) -> str:
    """Mailing sending process"""

    print("[*] Processing campaign", campaign_id)

    # Get campaign
    campaign = MailingCampaign.manager.get(id=campaign_id)
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

        print("[*] Processing email:", email)

        try:
            send_attempt_counter += 1
            smtp_service.send_email(
                connection=connection,
                email=email,
                alias=alias,
                subject=subject,
                html=html_content,
                text=text_content,
            )
        except TimeoutError as exception:
            print(f"[-] Timeout for `{email}`: {exception}")
            print("[*] Sleeping 10s ...")
            time.sleep(10)
            print(f"[*] Marking `{email}` as `BEING_PROCESSED`")
            pool_manager.change_status(document_id, MailingPoolStatus.BEING_PROCESSED)
            connection = smtp_service.get_smtp_connection()
        except SMTPServerDisconnected as exception:
            pool_manager.change_status(
                document_id, MailingPoolStatus.SMTP_SERVER_DISCONNECTED
            )
            print(f"[-] SMTPServerDisconnected: {exception}")
            connection = smtp_service.get_smtp_connection()
        except ConnectionRefusedError as exception:
            pool_manager.change_status(
                document_id, MailingPoolStatus.CONNECTION_REFUSED
            )
            print(f"[-] ConnectionRefusedError: {exception}")
            connection = smtp_service.get_smtp_connection()
        except SMTPRecipientsRefused as exception:
            pool_manager.change_status(
                document_id, MailingPoolStatus.CONNECTION_REFUSED
            )
            print(f"[-] SMTPRecipientsRefused: {exception}")
            connection = smtp_service.get_smtp_connection()
        else:
            pool_manager.change_status(document_id, MailingPoolStatus.SENT)
            print(f"[+] Sent to `{email}`")

            # Increment sent counter
            MailingCampaign.manager.filter(id=campaign_id).update(
                stat_sent=F("stat_sent") + 1
            )

            # Increment sent so far counter if limit per day set
            if campaign.limit_per_day != 0:
                MailingCampaign.manager.filter(id=campaign_id).update(
                    limit_sent_so_far=F("limit_sent_so_far") + 1
                )

    pool_manager.close()  # close mongo manager
    connection.close()  # close SMTP connection

    if send_attempt_counter == 0:
        return_value = ProcessSendingStatus.NO_EMAILS_SENT

    return return_value


def try_to_finish_campaign(campaign_id: int):
    """Try to finish campaign if there are no init-like emails left"""
    pool_manager = MailingPoolManager()
    campaign_is_finished = pool_manager.is_campaign_finished(campaign_id)
    if campaign_is_finished:
        print("[*] No init emails left, closing campaign:", campaign_id)

        MailingCampaign.manager.filter(id=campaign_id).update(
            status=MailingCampaignStatus.DONE
        )

        telegram_service = TelegramService()
        telegram_service.send_chat_message(
            f"Kampania mailingowa ID={campaign_id} zakończona",
            TelegramChats.OTHER,
        )

    pool_manager.close()


def try_to_reset_daily_limit_for_campaigns():
    """Try to reset daily limit for campaigns

    Reset `sent so far` counter for active campaigns that have limit
    set and 24h have passed

    Reset `limit_sent_so_far` to 0
    Set `limit_timestamp` to `now()`
    """
    # TODO: This doesn't work
    # TODO: Check manually if this works
    MailingCampaign.manager.active_campaigns().filter(
        ~Q(limit_per_day=0) & Q(limit_timestamp__lt=now() - timedelta(hours=24))
    ).update(limit_sent_so_far=0, limit_timestamp=now())


class Command(BaseCommand):
    """Mailing sending command

    - Send emails from active campaigns

    """

    help = "Mailing sending"

    def add_arguments(self, parser):
        pass

    def start_loop(self):
        """Start infinite loop"""
        last_reset_daily_limit = now() - timedelta(days=999)

        while True:
            #
            # Every 5 minutes try to reset daily limit for campaigns
            if now() > last_reset_daily_limit:
                last_reset_daily_limit = now() + timedelta(minutes=5)
                try_to_reset_daily_limit_for_campaigns()
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
                print("\n[*] Processing campaign:", campaign)
                result = process_sending(campaign_id, limit=100)
                #
                # Try to finish campaign
                if result == ProcessSendingStatus.NO_EMAILS_SENT:
                    print("[*] No email sent with campaign:", campaign)
                    try_to_finish_campaign(campaign_id)

            print("[*] Sleeping 3s between sending ...")
            time.sleep(3)

    def handle(self, *args, **options):
        self.start_loop()
