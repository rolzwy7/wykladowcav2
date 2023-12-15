# flake8: noqa=E501

from django.urls import path

from core.views.conference import conference_cycle_page, conference_edition_page

urlpatterns = [
    path(
        "<slug:slug_cycle>/",
        conference_cycle_page,
        name="conference_cycle_page",
    ),
    path(
        "<slug:slug_cycle>/<slug:slug_edition>/",
        conference_edition_page,
        name="conference_edition_page",
    ),
]
