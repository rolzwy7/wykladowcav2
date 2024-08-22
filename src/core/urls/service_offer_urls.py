from django.urls import path

from core.views.service_offer import service_offer_page

urlpatterns = [
    path(
        "<slug:slug>/",
        service_offer_page,
        name="service_offer_page",
    ),
]
