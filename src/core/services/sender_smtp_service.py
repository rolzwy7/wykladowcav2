"""Sender SMTP service"""

# flake8: noqa=E501

from poplib import POP3_SSL, error_proto
from typing import Iterable, Optional

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend

from core.models.mailing import MailingCampaign, SmtpSender


class SenderSmtpService:
    """SMTP sender service"""

    def __init__(self, smtp_sender: SmtpSender) -> None:
        self.smtp_sender = smtp_sender

    def get_pop3_instance(self) -> POP3_SSL:
        """Returns `POP3_SSL` instance configured for this sender"""
        pop3 = POP3_SSL(
            self.smtp_sender.incoming_server_hostname,
            int(self.smtp_sender.incoming_server_port),
        )
        pop3.user(self.smtp_sender.return_path)
        pop3.pass_(self.smtp_sender.password)
        return pop3

    def get_inbox_messages(
        self, pop3: POP3_SSL
    ) -> Iterable[tuple[int, list[bytes], bytes]]:
        """Yields messages from POP3 connection"""

        num_messages, _ = pop3.stat()

        for message_idx in range(1, num_messages + 1):
            _, message_lines, _ = pop3.retr(message_idx)
            message_bytes = b"\n".join(message_lines)
            yield (message_idx, message_lines, message_bytes)

    def get_smtp_connection(self, timeout: int = 5):
        """Get SMTP connection or this sender"""
        sender = self.smtp_sender
        return EmailBackend(
            host=sender.outgoing_server_hostname,
            port=sender.outgoing_server_port,
            username=sender.username,
            password=sender.password,
            use_ssl=sender.ssl,
            timeout=timeout,
        )

    def send_email(
        self,
        /,
        connection: EmailBackend,
        email: str,
        alias: str,
        subject: str,
        html: str,
        text: str,
        resignation_url: str,
        resignation_path: str,
        tracking_code: str,
        campaign_id: int,
        cc=None,
        bcc=None,
        test_subject_id=None,
    ):
        """Send email message"""

        from_email = f'"{alias}" <{self.smtp_sender.username}>'
        to_email = email
        text_content = text
        html_content = html
        list_unsubscribe = f"<mailto:{from_email}?subject=Rezygnacja {email}>"
        reply_to = self.smtp_sender.reply_to

        headers = {
            "Precedence": "bulk",
            "List-Unsubscribe": list_unsubscribe,
            "Reply-To": reply_to,
        }

        html_content = html_content.replace("{ODBIORCA#ADRES}", "{TO_EMAIL}")
        text_content = text_content.replace("{ODBIORCA#ADRES}", "{TO_EMAIL}")

        html_content = html_content.replace("{TO_EMAIL}", to_email)
        text_content = text_content.replace("{TO_EMAIL}", to_email)

        html_content = html_content.replace("{SUB_URL}", to_email)
        text_content = text_content.replace("{SUB_URL}", to_email)

        html_content = html_content.replace("{RESIGNATION_URL}", resignation_url)
        text_content = text_content.replace("{RESIGNATION_URL}", resignation_url)

        html_content = html_content.replace("{RESIGNATION_PATH}", resignation_path)
        text_content = text_content.replace("{RESIGNATION_PATH}", resignation_path)

        html_content = html_content.replace("{TRACKING_CODE}", tracking_code)
        text_content = text_content.replace("{TRACKING_CODE}", tracking_code)

        html_content = html_content.replace("{CAMPAIGN_ID}", str(campaign_id))
        text_content = text_content.replace("{CAMPAIGN_ID}", str(campaign_id))

        html_content = html_content.replace("{TEST_SUBJECT_ID}", str(test_subject_id))
        text_content = text_content.replace("{TEST_SUBJECT_ID}", str(test_subject_id))

        # Resolve base url for template
        base_url = settings.BASE_URL
        if campaign_id != 0:
            camp_qs = MailingCampaign.manager.filter(id=campaign_id)
            if camp_qs.exists():
                campaign: MailingCampaign = camp_qs.first()  # type: ignore

                if campaign.base_url_override:
                    base_url = campaign.base_url_override
                    html_content = html_content.replace(
                        settings.BASE_URL, campaign.base_url_override
                    )
                    text_content = text_content.replace(
                        settings.BASE_URL, campaign.base_url_override
                    )

                if campaign.smtp_sender.return_path:
                    headers["Return-Path"] = campaign.smtp_sender.return_path

        html_content = html_content.replace("{DOMAIN}", base_url)
        text_content = text_content.replace("{DOMAIN}", base_url)

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            headers=headers,
            to=[to_email],
            cc=cc,
            bcc=bcc,
            connection=connection,
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
