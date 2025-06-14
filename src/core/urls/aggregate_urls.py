"""
Webinar URLs
"""

# flake8: noqa=E501

from django.urls import path

from core.views.webinar import aggregate_ogimage_page, webinar_aggregate_page
from core.views.webinar.webinar_queue_endpoint import webinar_queue_endpoint

urlpatterns = [
    path("<slug:slug>/", webinar_aggregate_page, name="webinar_aggregate_page"),
    path(
        "<str:grouping_token>/og-image.png",
        aggregate_ogimage_page,
        name="aggregate_ogimage_page",
    ),
    # Kolejka
    path(
        "queue/<str:grouping_token>/",
        webinar_queue_endpoint,
        name="webinar_queue_endpoint",
    ),
]
