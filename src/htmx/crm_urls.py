"""HTMX CRM URL"""

# flake8: noqa=E501
from django.urls import path

from htmx.views.crm import (
    htmx_conference_url_form,
    htmx_crm_application_cancellation_toggle,
    htmx_crm_check_nip,
    htmx_crm_delete_webinar_asset,
    htmx_crm_email_tagging_init,
    htmx_crm_email_tagging_toggle,
    htmx_crm_participant_indicators,
    htmx_crm_participant_toggle_phoned,
    htmx_crm_participant_toggle_uncertain,
    htmx_crm_toggle_todo,
)

urlpatterns = [
    path(
        "conference-url-form/<int:pk>/<str:mode>/",
        htmx_conference_url_form,
        name="htmx_conference_url_form",
    ),
    path(
        "application-cancellation-toggle/<int:pk>",
        htmx_crm_application_cancellation_toggle,
        name="htmx_crm_application_cancellation_toggle",
    ),
    path(
        "participant-indicators/<int:pk>",
        htmx_crm_participant_indicators,
        name="htmx_crm_participant_indicators",
    ),
    path(
        "participant-toggle-phoned/<int:pk>",
        htmx_crm_participant_toggle_phoned,
        name="htmx_crm_participant_toggle_phoned",
    ),
    path(
        "participant-toggle-uncertain/<int:pk>",
        htmx_crm_participant_toggle_uncertain,
        name="htmx_crm_participant_toggle_uncertain",
    ),
    path(
        "delete-webinar-asset/<int:pk>",
        htmx_crm_delete_webinar_asset,
        name="htmx_crm_delete_webinar_asset",
    ),
    path(
        "todo/<int:pk>/toggle",
        htmx_crm_toggle_todo,
        name="htmx_crm_toggle_todo",
    ),
    path(
        "tag-email/<str:email>",
        htmx_crm_email_tagging_init,
        name="htmx_crm_email_tagging_init",
    ),
    path(
        "toggle-tag/<str:email>/<str:tag>",
        htmx_crm_email_tagging_toggle,
        name="htmx_crm_email_tagging_toggle",
    ),
    path(
        "crm-check-nip/<str:nip>/",
        htmx_crm_check_nip,
        name="htmx_crm_check_nip",
    ),
]
