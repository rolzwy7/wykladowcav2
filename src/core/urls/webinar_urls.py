from django.urls import path

from core.views import (
    webinar_lecturer_biography_page,
    webinar_opinions_page,
    webinar_price_and_invoice_page,
    webinar_program_page,
)
from core.views.webinar_cancellation import webinar_cancellation_page

urlpatterns = [
    path("<slug:slug>/", webinar_program_page, name="webinar_program_page"),
    path(
        "<slug:slug>/opinie/",
        webinar_opinions_page,
        name="webinar_opinions_page",
    ),
    path(
        "<slug:slug>/cena-i-faktura/",
        webinar_price_and_invoice_page,
        name="webinar_price_and_invoice_page",
    ),
    path(
        "<slug:slug>/o-wykladowcy/",
        webinar_lecturer_biography_page,
        name="webinar_lecturer_biography_page",
    ),
    path(
        "potwierdzenie-odwolania-szkolenia/<uuid:token>/",
        webinar_cancellation_page,
        name="webinar_cancellation_page",
    ),
]
