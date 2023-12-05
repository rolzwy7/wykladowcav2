"""
Webinar URLs
"""

from django.urls import path

from core.views.webinar import (
    webinar_certificate_page,
    webinar_faq_page,
    webinar_loyalty_program_page,
    webinar_ogimage_page,
    webinar_opinions_page,
    webinar_price_and_invoice_page,
    webinar_program_page,
    webinar_redirect_to_application,
    webinar_redirect_to_program,
    webinar_redirect_to_program_facebook,
    webinar_redirect_to_program_onesignal,
)
from core.views.webinar_cancellation import webinar_cancellation_page
from core.views.webinar_moving import (
    webinar_moving_accept_page,
    webinar_moving_resignation_page,
    webinar_moving_thanks_page,
)

urlpatterns = [
    # Webinar redirects
    path(
        "<int:pk>/",
        webinar_redirect_to_program,
        name="webinar_redirect_to_program",
    ),
    path(
        "<int:pk>/facebook/",
        webinar_redirect_to_program_facebook,
        name="webinar_redirect_to_program_facebook",
    ),
    path(
        "<int:pk>/push-onesignal/",
        webinar_redirect_to_program_onesignal,
        name="webinar_redirect_to_program_onesignal",
    ),
    path(
        "<int:pk>/zgloszenie/",
        webinar_redirect_to_application,
        name="webinar_redirect_to_application",
    ),
    # Webinar by slug
    path("<slug:slug>/", webinar_program_page, name="webinar_program_page"),
    path(
        "<slug:slug>/opinie/",
        webinar_opinions_page,
        name="webinar_opinions_page",
    ),
    path(
        "<slug:slug>/certyfikat/",
        webinar_certificate_page,
        name="webinar_certificate_page",
    ),
    path(
        "<slug:slug>/cena-i-faktura/",
        webinar_price_and_invoice_page,
        name="webinar_price_and_invoice_page",
    ),
    path(
        "<slug:slug>/polecja-i-zarabiaj/",
        webinar_loyalty_program_page,
        name="webinar_loyalty_program_page",
    ),
    path(
        "<slug:slug>/faq/",
        webinar_faq_page,
        name="webinar_faq_page",
    ),
    # og:image
    path(
        "<int:pk>/og-image.png",
        webinar_ogimage_page,
        name="webinar_ogimage_page",
    ),
    # Cancellation TODO: move this
    path(
        "potwierdzenie-odwolania-szkolenia/<uuid:token>/",
        webinar_cancellation_page,
        name="webinar_cancellation_page",
    ),
    # Moving TODO: move this
    path(
        "<uuid:token>/akceptacja-nowego-terminu/",
        webinar_moving_accept_page,
        name="webinar_moving_accept_page",
    ),
    path(
        "<uuid:token>/rezygnacja-z-nowego-terminu/",
        webinar_moving_resignation_page,
        name="webinar_moving_resignation_page",
    ),
    path(
        "<uuid:token>/dziekujemy-za-odp-przenoszenie-szkol/",
        webinar_moving_thanks_page,
        name="webinar_moving_thanks_page",
    ),
]
