from django.urls import path

from core.views.crm import (
    crm_invoice_email_preview,
    crm_participant_certificate_email_preview,
    crm_participant_confirmation_email_preview,
    crm_participant_opinion_email_preview,
    crm_participant_preparation_email_preview,
    crm_submitter_cancellation_email_preview,
    crm_submitter_confirmation_email_preview,
)

urlpatterns = [
    path(
        "submitter-cancellation-email-preview/",
        crm_submitter_cancellation_email_preview,
        name="crm_submitter_cancellation_email_preview",
    ),
    path(
        "submitter-confirmation-email-preview/",
        crm_submitter_confirmation_email_preview,
        name="crm_submitter_confirmation_email_preview",
    ),
    path(
        "participant-confirmation-email-preview/",
        crm_participant_confirmation_email_preview,
        name="crm_participant_confirmation_email_preview",
    ),
    path(
        "participant-certificate-email-preview/",
        crm_participant_certificate_email_preview,
        name="crm_participant_certificate_email_preview",
    ),
    path(
        "invoice-email-preview/",
        crm_invoice_email_preview,
        name="crm_invoice_email_preview",
    ),
    path(
        "participant-preparation-email-preview/",
        crm_participant_preparation_email_preview,
        name="crm_participant_preparation_email_preview",
    ),
    path(
        "participant-opinion-email-preview/",
        crm_participant_opinion_email_preview,
        name="crm_participant_opinion_email_preview",
    ),
]
