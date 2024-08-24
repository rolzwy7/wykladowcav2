"""Service Offer URLs"""

# flake8: noqa=E501

from django.urls import path

from core.views.service_offer import service_offer_page, service_offer_thanks_page

urlpatterns = [
    path(
        "<slug:slug>/dziekujemy/",
        service_offer_thanks_page,
        name="service_offer_thanks_page",
    ),
    path(
        "<slug:slug>/",
        service_offer_page,
        name="service_offer_page",
    ),
]
