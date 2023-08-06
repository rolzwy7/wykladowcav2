from core.libs.inbox import InboxMessage
from core.models.mailing import SmtpSender
from core.services import SenderSmtpService


class SenderMailboxService:
    """Service for handling sender's mailbox"""

    def __init__(self, smtp_sender: SmtpSender) -> None:
        self.smtp_sender = smtp_sender

    def process_vacation_messages(self):
        """Process vacation messages

        Iterate over mailbox messages. Save bounces.
        """
        service = SenderSmtpService(self.smtp_sender)
        pop3 = service.get_pop3_instance()

        for _, _, msg_bytes in service.get_inbox_messages(pop3):
            inbox_message = InboxMessage(msg_bytes)

            # if inbox_message.is_vacation(): TODO
            #     obj, created = BlacklistedTemporary.objects.get_or_create(
            #         inbox_id=email_message.unique_hash,
            #         email=email_message.from_email,
            #         email_content=email_message.get_content(),
            #     )

    # def process_bounce_messages(self):
    #     """Process bounce messages

    #     Iterate over mailbox messages. Save bounces.
    #     """
    #     service = SenderSmtpService(self.smtp_sender)
    #     pop3 = service.get_pop3_instance()
    #     for _, _, msg_bytes in service.get_inbox_messages(pop3):
    #         email_message = EmailMessage(msg_bytes)

    #         # Save permanent failures
    #         for email in email_message.permanent_failures:
    #             EmailBounce.objects.get_or_create(
    #                 smtp_sender=smtp_sender,
    #                 bounce_type=EmailBounce.PERMANENT,
    #                 email=email,
    #                 email_message=email_message.get_content(),
    #                 email_id=email_message.message_id_header,
    #             )

    #         # Save temporary failures
    #         for email in email_message.temporary_failures:
    #             EmailBounce.objects.get_or_create(
    #                 smtp_sender=smtp_sender,
    #                 bounce_type=EmailBounce.TEMPORARY,
    #                 email=email,
    #                 email_message=email_message.get_content(),
    #                 email_id=email_message.message_id_header,
    #             )
