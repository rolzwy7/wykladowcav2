from django.urls import path

from core.views.crm import (
    crm_participant_confirmation_email_preview,
    crm_submitter_confirmation_email_preview,
)

urlpatterns = [
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
]
