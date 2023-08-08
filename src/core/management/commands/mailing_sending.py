import time
from smtplib import SMTPServerDisconnected

from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand

from core.models import (
    MailingCampaign,
    MailingPoolManager,
    MailingTemplate,
    SmtpSender,
)
from core.models.enums import MailingPoolStatus
from core.services import SenderSmtpService


def process_sending(campaign: MailingCampaign):
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

    print("Processing campign", campaign_id)

    for document in documents:
        subject = campaign.get_random_subject()
        from_email = smtp_sender.username
        email = document["email"]
        document_id = f"{campaign_id}:{email}"
        to_email = f"{alias} <{email}>"
        text_content = text
        html_content = html
        list_unsubscribe = f"<mailto:{from_email}?subject=Rezygnacja {email}>"

        print("Sending to:", email)

        try:
            with smtp_service.get_smtp_connection() as connection:
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=from_email,
                    headers={
                        "List-Unsubscribe": list_unsubscribe,
                        "Reply-To": smtp_sender.reply_to,
                    },
                    to=[to_email],
                    connection=connection,
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
        except SMTPServerDisconnected:
            pool_manager.change_status(
                document_id, MailingPoolStatus.SMTP_SERVER_DISCONNECTED
            )
        else:
            pool_manager.change_status(document_id, MailingPoolStatus.SENT)

        print("done test")
        exit(0)

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

        loop_counter = 0

        while True:
            # Get all active campaigns
            active_campaigns = MailingCampaign.manager.active_campaigns()
            print("active_campaigns:", active_campaigns)

            for campaign in active_campaigns:
                process_sending(campaign)

            loop_counter += 1
            exit(0)  # TODO
            print("waiting 5 seconds ...")
            time.sleep(5)

    def handle(self, *args, **options):
        self.start_loop()
