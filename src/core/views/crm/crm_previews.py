from django.http import HttpResponse
from django.urls import reverse
from django.utils.timezone import now, timedelta

from core.libs.notifications.email import (
    EmailTemplate,
    email_get_application_context,
)
from core.models import WebinarApplication, WebinarCertificate, WebinarMetadata


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
    application = WebinarApplication.manager.all().order_by("?").first()
    if not application:
        return HttpResponse("No application present in database")

    email_template = EmailTemplate(
        "email/EmailParticipantConfirmation.html",
        email_get_application_context(application.id),  # type: ignore,
    )
    return HttpResponse(email_template.get_html())


def crm_participant_certificate_email_preview(request):
    """Preview of certificate email send to participant after webinar done"""
    application = WebinarApplication.manager.all().order_by("?").first()
    certificates = WebinarCertificate.objects.all()

    if certificates.exists():
        certificate = certificates.order_by("?").first()
        certificate_url = certificate.get_absolute_url()  # type: ignore
    else:
        certificate_url = "#certificate_url"

    application_id: int = application.id  # type: ignore
    email_template = EmailTemplate(
        "email/EmailParticipantCertificate.html",
        {
            "certificate_url": certificate_url,
            **email_get_application_context(application_id),
        },
    )
    return HttpResponse(email_template.get_html())


def crm_invoice_email_preview(request):
    """Preview invoice email"""
    application = WebinarApplication.manager.all().order_by("?")
    application_id: int = application.first().id  # type: ignore
    email_template = EmailTemplate(
        "email/EmailInvoice.html",
        {
            "invoice_number": "12345",
            **email_get_application_context(application_id),
        },
    )
    return HttpResponse(email_template.get_html())


def crm_participant_preparation_email_preview(request):
    """Preview of preparation email"""
    application = WebinarApplication.manager.all().order_by("?").first()
    if not application:
        return HttpResponse("No application present in database")

    webinar_metadata = WebinarMetadata.objects.get(webinar=application.webinar)

    assets_url = reverse(
        "core:webinar_assets_page",
        kwargs={"uuid": webinar_metadata.assets_token},
    )

    email_template = EmailTemplate(
        "email/EmailParticipantPreparation.html",
        {
            **email_get_application_context(application.id),  # type: ignore
            "assets_url": assets_url,
        },
    )
    return HttpResponse(email_template.get_html())


def crm_participant_opinion_email_preview(request):
    """Preview of opinion e-mail"""
    application = WebinarApplication.manager.all().order_by("?")
    application_id: int = application.first().id  # type: ignore
    email_template = EmailTemplate(
        "email/EmailParticipantOpinion.html",
        {**email_get_application_context(application_id)},
    )
    return HttpResponse(email_template.get_html())


def crm_submitter_cancellation_email_preview(request):
    """Preview of opinion e-mail"""
    application = WebinarApplication.manager.all().order_by("?")
    application_id: int = application.first().id  # type: ignore
    email_template = EmailTemplate(
        "email/EmailSubmitterCancellation.html",
        {
            **email_get_application_context(application_id),
            "cancellation_token": "dda34d5e-c50b-4cca-8864-19c1463acba3",
        },
    )
    return HttpResponse(email_template.get_html())


def crm_submitter_moving_email_preview(request):
    """Preview of opinion e-mail"""
    application = WebinarApplication.manager.all().order_by("?")
    application_id: int = application.first().id  # type: ignore
    email_template = EmailTemplate(
        "email/EmailSubmitterMoving.html",
        {
            **email_get_application_context(application_id),
            "old_date": now(),
            "new_date": now() + timedelta(days=7),
            "token": "dda34d5e-c50b-4cca-8864-19c1463acba3",
        },
    )
    return HttpResponse(email_template.get_html())


def crm_registration_email_preview(request):
    """Preview of registration e-mail"""
    email_template = EmailTemplate(
        "email/EmailRegistration.html",
        {
            "activation_token": "[ACTIVATION_TOKEN]",
        },
    )
    return HttpResponse(email_template.get_html())
