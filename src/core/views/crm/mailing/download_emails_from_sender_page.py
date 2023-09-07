import logging
import re

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page

from core.libs.inbox import InboxMessage
from core.models import SmtpSender
from core.services import SenderSmtpService

EMAIL_PATTERN = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

logging.getLogger("flufl.bounce").setLevel(logging.WARNING)


@cache_page(60 * 15)
def download_emails_from_sender_page(request, pk: int, export_type: str):
    """Download email from sender inbox"""
    smtp_sender = get_object_or_404(SmtpSender, pk=pk)
    smtp_service = SenderSmtpService(smtp_sender)
    pop3 = smtp_service.get_pop3_instance()

    emails = []

    for message in smtp_service.get_inbox_messages(pop3):
        _, _, message_bytes = message
        inbox_message = InboxMessage(message_bytes)

        if export_type == "permanent":
            for email in inbox_message.get_emails_permanent_failure():
                emails.append(email)

        if export_type == "temporary":
            for email in inbox_message.get_emails_temporary_failure():
                emails.append(email)

        if export_type == "emails_in_message":
            content = inbox_message.get_content()
            emails.extend(re.findall(EMAIL_PATTERN, content))

    emails = list(set(emails))

    return HttpResponse("\n".join(emails), content_type="text/plain")
