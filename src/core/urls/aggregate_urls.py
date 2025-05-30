"""
Webinar URLs
"""

# flake8: noqa=E501

from django.urls import path

from core.views.webinar import webinar_aggregate_page

urlpatterns = [
    path("<slug:slug>/", webinar_aggregate_page, name="webinar_aggregate_page"),
]
