from django.urls import path

from htmx.views import (
    application_discount_panel,
    crm_lecturer_price_card,
    htmx_delete_webinar_asset,
    htmx_toggle_crm_todo,
)

app_name = "htmx"

urlpatterns = [
    path(
        "crm-delete-webinar-asset/<int:pk>/",
        htmx_delete_webinar_asset,
        name="htmx_delete_webinar_asset",
    ),
    path(
        "crm-todo/<int:pk>/toggle",
        htmx_toggle_crm_todo,
        name="htmx_toggle_crm_todo",
    ),
    path(
        "crm-lecturer-price-card/<int:webinar_pk>/<str:mode>/",
        crm_lecturer_price_card,
        name="crm_lecturer_price_card",
    ),
    path(
        "application-discount-summary/<int:pk>/",
        application_discount_panel,
        name="htmx_application_discount_panel",
    ),
]
