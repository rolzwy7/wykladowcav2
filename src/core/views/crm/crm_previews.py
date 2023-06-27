from django.http import HttpResponse

from core.libs.notifications.email import EmailTemplate


def crm_submitter_confirmation_email_preview(request):
    """Preview of email send to submitter after application send"""
    email_template = EmailTemplate("email/EmailSubmitterConfirmation.html", {})
    return HttpResponse(email_template.html)
