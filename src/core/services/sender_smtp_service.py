from poplib import POP3_SSL
from typing import Iterable

from django.core.mail.backends.smtp import EmailBackend

from core.models.mailing import SmtpSender


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
            message_lines = pop3.retr(message_idx)[1]
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
