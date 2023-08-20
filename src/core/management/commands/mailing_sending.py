import time
from smtplib import SMTPServerDisconnected

from django.core.management.base import BaseCommand

from core.models import (
    MailingCampaign,
    MailingPoolManager,
    MailingTemplate,
    SmtpSender,
)
from core.models.enums import MailingCampaignStatus, MailingPoolStatus
from core.services import SenderSmtpService


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
        except SMTPServerDisconnected as exception:
            pool_manager.change_status(
                document_id, MailingPoolStatus.SMTP_SERVER_DISCONNECTED
            )
            print(f"[-] SMTPServerDisconnected: {exception}")
        else:
            pool_manager.change_status(document_id, MailingPoolStatus.SENT)
            print(f"[+] Sent to `{email}`")

    pool_manager.close()  # close mongo manager
    connection.close()  # close SMTP connection

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
    pool_manager.close()


class Command(BaseCommand):
    """Mailing sending command

    - Send emails from active campaigns

    """

    help = "Mailing sending"

    def add_arguments(self, parser):
        pass

    def start_loop(self):
        """Start infinite loop"""

        while True:
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
