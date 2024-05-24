# flake8: noqa=E501

from django.urls import path

from core.views.conference import (
    conference_cycle_page,
    conference_edition_page,
    conference_edition_redirect_page,
    conference_edition_thanks_page,
)

urlpatterns = [
    path(
        "cykl-szkolen/<slug:slug_cycle>/",
        conference_cycle_page,
        name="conference_cycle_page",
    ),
    path(
        "p/<uuid:uuid>/",
        conference_edition_redirect_page,
        name="conference_edition_redirect_page",
    ),
    path(
        "<slug:slug_edition>/dziekujemy/",
        conference_edition_thanks_page,
        name="conference_edition_thanks_page",
    ),
    path(
        "<slug:slug_edition>/",
        conference_edition_page,
        name="conference_edition_page",
    ),
]
