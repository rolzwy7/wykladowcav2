from poplib import POP3_SSL, error_proto
from typing import Iterable

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend
from django.urls import reverse

from core.models.mailing import SmtpSender
from core.services.mailing import MailingResignationService

BASE_URL = settings.BASE_URL


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
        pop3.user(self.smtp_sender.username)
        pop3.pass_(self.smtp_sender.password)
        return pop3

    def get_inbox_messages(
        self, pop3: POP3_SSL
    ) -> Iterable[tuple[int, list[bytes], bytes]]:
        """Yields messages from POP3 connection"""
        num_octet_pairs = pop3.list()[1]
        for _idx, _ in enumerate(num_octet_pairs):
            message_idx = _idx + 1

            try:
                message_lines = pop3.retr(message_idx)[1]
            except error_proto:
                message_lines = [f"MESSAGE_IDX_{message_idx}".encode()]

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
    ):
        """Send email message"""

        from_email = f'"{alias}" <{self.smtp_sender.username}>'
        to_email = email
        text_content = text
        html_content = html
        list_unsubscribe = f"<mailto:{from_email}?subject=Rezygnacja {email}>"
        reply_to = self.smtp_sender.reply_to

        # TODO: temporary solution
        resignation_code = (
            MailingResignationService.get_or_create_inactive_resignation(email)
        )
        resignation_url = BASE_URL + reverse(
            "core:mailing_resignation_page",
            kwargs={"resignation_code": resignation_code},
        )

        # TODO: temporary solution
        html_content = html_content.replace("{ODBIORCA#ADRES}", "{TO_EMAIL}")
        text_content = text_content.replace("{ODBIORCA#ADRES}", "{TO_EMAIL}")

        html_content = html_content.replace("{TO_EMAIL}", to_email)
        text_content = text_content.replace("{TO_EMAIL}", to_email)

        # TODO: temporary solution
        html_content = html_content.replace("{SUB_URL}", to_email)
        text_content = text_content.replace("{SUB_URL}", to_email)

        # TODO: temporary solution
        html_content = html_content.replace(
            "{RESIGNATION_URL}", resignation_url
        )
        text_content = text_content.replace(
            "{RESIGNATION_URL}", resignation_url
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            headers={
                "Precedence": "bulk",
                "List-Unsubscribe": list_unsubscribe,
                "Reply-To": reply_to,
            },
            to=[to_email],
            connection=connection,
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
