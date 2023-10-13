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

    permanent_failures = []
    temporary_failures = []
    emails_in_content = []

    for message in smtp_service.get_inbox_messages(pop3):
        _, _, message_bytes = message
        inbox_message = InboxMessage(message_bytes)

        for email in inbox_message.get_emails_permanent_failure():
            permanent_failures.append(email)

        for email in inbox_message.get_emails_temporary_failure():
            temporary_failures.append(email)

        content = inbox_message.get_content()
        emails_in_content.extend(re.findall(EMAIL_PATTERN, content))

    pop3.close()

    if export_type == "permanent":
        permanent_failures = list(set(permanent_failures))
        return HttpResponse(
            "\n".join(permanent_failures), content_type="text/plain"
        )

    if export_type == "temporary":
        temporary_failures = list(set(temporary_failures))
        return HttpResponse(
            "\n".join(temporary_failures), content_type="text/plain"
        )

    if export_type == "question_emails":
        question_emails = []
        for email in emails_in_content:
            if all(
                [
                    email not in permanent_failures,
                    email not in temporary_failures,
                ]
            ):
                question_emails.append(email)

        question_emails = list(set(question_emails))
        return HttpResponse(
            "\n".join(question_emails), content_type="text/plain"
        )

    return HttpResponse("Invalid request", content_type="text/plain")
