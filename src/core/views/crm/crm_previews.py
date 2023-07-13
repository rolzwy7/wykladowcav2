from django.http import HttpResponse

from core.libs.notifications.email import (
    EmailTemplate,
    email_get_application_context,
)
from core.models import WebinarApplication


def crm_submitter_confirmation_email_preview(request):
    """Preview of email send to submitter after application send"""
    application = WebinarApplication.manager.all().order_by("?")
    email_template = EmailTemplate(
        "email/EmailSubmitterConfirmation.html",
        email_get_application_context(application.first().id),  # type: ignore
    )
    return HttpResponse(email_template.get_html())


def crm_participant_confirmation_email_preview(request):
    """Preview of email send to submitter after application send"""
    application = WebinarApplication.manager.all().order_by("?")
    email_template = EmailTemplate(
        "email/EmailParticipantConfirmation.html",
        email_get_application_context(application.first().id),  # type: ignore
    )
    return HttpResponse(email_template.get_html())
