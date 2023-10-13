from django.urls import path

from htmx.views.crm import (
    htmx_crm_application_cancellation_toggle,
    htmx_crm_delete_webinar_asset,
    htmx_crm_email_tagging_init,
    htmx_crm_email_tagging_toggle,
    htmx_crm_lecturer_price_card,
    htmx_crm_participant_indicators,
    htmx_crm_participant_toggle_phoned,
    htmx_crm_toggle_todo,
)

urlpatterns = [
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
        "lecturer-price-card/<int:webinar_pk>/<str:mode>",
        htmx_crm_lecturer_price_card,
        name="htmx_crm_lecturer_price_card",
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
]
