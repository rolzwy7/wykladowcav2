import time
from smtplib import SMTPRecipientsRefused, SMTPServerDisconnected

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.timezone import now, timedelta

from core.consts import TelegramChats
from core.models import (
    MailingCampaign,
    MailingPoolManager,
    MailingTemplate,
    SmtpSender,
)
from core.models.enums import MailingCampaignStatus, MailingPoolStatus
from core.services import SenderSmtpService, TelegramService


class ProcessSendingStatus:
    """Process sending status"""

    NO_EMAILS_SENT = "NO_EMAILS_SENT"
    LIMIT_REACHED = "LIMIT_REACHED"
    LIMIT_NOT_REACHED = "LIMIT_NOT_REACHED"


def process_sending(campaign: MailingCampaign, limit: int = 100) -> str:
    """Mailing sending process"""

    campaign_id: int = campaign.id  # type: ignore
    alias = campaign.alias

    template: MailingTemplate = campaign.template
    html = template.html
    text = template.text

    smtp_sender: SmtpSender = campaign.smtp_sender
    smtp_service = SenderSmtpService(smtp_sender)

    pool_manager = MailingPoolManager()
    documents = pool_manager.get_ready_to_send_for_campaign(campaign_id)

    print("[*] Processing campaign", campaign_id)

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
            pool_manager.change_status(
                document_id, MailingPoolStatus.BEING_PROCESSED
            )
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
            campaign.stat_sent = campaign.stat_sent + 1

            # Increment sent so far counter if limit per day set
            if campaign.limit_per_day != 0:
                campaign.limit_sent_so_far = campaign.limit_sent_so_far + 1
        finally:
            # Increment procesed counter
            campaign.stat_procesed = campaign.stat_procesed + 1

    pool_manager.close()  # close mongo manager
    connection.close()  # close SMTP connection
    campaign.save()

    if send_attempt_counter == 0:
        return_value = ProcessSendingStatus.NO_EMAILS_SENT

    return return_value


def try_to_finish_campaign(campaign: MailingCampaign):
    """Try to finish campaign if there are no init-like emails left"""
    campaign_id: int = campaign.id  # type: ignore
    pool_manager = MailingPoolManager()
    campaign_is_finished = pool_manager.is_campaign_finished(campaign_id)
    if campaign_is_finished:
        print("[*] No init emails left, closing campaign:", campaign)
        campaign.status = MailingCampaignStatus.DONE
        campaign.save()

        telegram_service = TelegramService()
        telegram_service.send_chat_message(
            f"Kampania mailignowa zakończona: {campaign.title}",
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
        loop_counter = 0

        while True:
            # Increment loop counter and apply modulo
            loop_counter += 1
            loop_counter = loop_counter % 10_000

            # Try to reset daily limit for campaigns
            # Run on first and every 20th loop
            if loop_counter == 1 or loop_counter % 20 == 0:
                try_to_reset_daily_limit_for_campaigns()

            # Get all active mailing campaigns
            active_campaigns = MailingCampaign.manager.active_campaigns()

            # Sleep and continue loop if no active campaigns
            if active_campaigns.count() == 0:
                print("[*] No active campaigns, sleeping 60s ...")
                time.sleep(60)
                continue

            # Iterate over active campaigns and start sending process
            for campaign in active_campaigns:
                print("\n[*] Processing campaign:", campaign)
                result = process_sending(campaign, limit=100)

                # Try to finish campaign
                if result == ProcessSendingStatus.NO_EMAILS_SENT:
                    print("[*] No email sent with campaign:", campaign)
                    try_to_finish_campaign(campaign)

            print("[*] Sleeping 5s between sending ...")
            time.sleep(5)

    def handle(self, *args, **options):
        self.start_loop()
