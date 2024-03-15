from django.urls import path

from htmx.views.application import htmx_application_discount_panel

urlpatterns = [
    path(
        "discount-summary/<int:pk>",
        htmx_application_discount_panel,
        name="htmx_application_discount_panel",
    ),
]
