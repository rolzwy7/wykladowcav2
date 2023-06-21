from django.urls import path

from core.views.webinar_application import (
    application_buyer_page,
    application_invoice_page,
    application_submitter_page,
    application_type_page,
)

urlpatterns = [
    path(
        "<int:pk>/typ-zgloszenia/",
        application_type_page,
        name="application_type_page",
    ),
    path(
        "<uuid:uuid>/nabywca/",
        application_buyer_page,
        name="application_buyer_page",
    ),
    path(
        "<uuid:uuid>/faktura/",
        application_invoice_page,
        name="application_invoice_page",
    ),
    path(
        "<uuid:uuid>/osoba-zglaszajaca/",
        application_submitter_page,
        name="application_submitter_page",
    ),
]
