"""CRM Inbox Page"""

# flake8: noqa=E501

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import MailingReplyMessage

BASE_URL = settings.BASE_URL


def crm_inbox_page(request):
    """CRM Inbox Page"""
    template_name = "core/pages/crm/inbox/CrmInboxPage.html"
    messages = MailingReplyMessage.manager.filter(checked=False)

    return TemplateResponse(
        request,
        template_name,
        {"messages": messages, "all_emails_count": messages.count()},
    )


def crm_inbox_message_page(request, email_id: str):
    """CRM Inbox Message Page"""
    message = get_object_or_404(MailingReplyMessage, email_id=email_id)
    return HttpResponse(
        message.message_content, content_type="text/html; charset=utf-8"
    )
