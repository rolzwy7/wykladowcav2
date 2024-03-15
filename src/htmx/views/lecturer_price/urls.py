"""HTMX URLs"""

# flake8: noqa=E501

from django.urls import path

from .panel import panel

app_name = "lecturer-price"  # pylint: disable=invalid-name

urlpatterns = [
    path(
        "panel/<int:webinar_pk>/<str:mode>/",
        panel,
        name="panel",
    ),
]
