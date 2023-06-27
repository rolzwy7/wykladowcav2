from django.urls import path

from core.views.crm.crm_previews import crm_submitter_confirmation_email_preview

urlpatterns = [
    path(
        "submitter-confirmation-preview/",
        crm_submitter_confirmation_email_preview,
        name="crm_submitter_confirmation_preview",
    )
]
