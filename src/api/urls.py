"""API urls"""

# flake8: noqa=E501

from django.urls import include, path

from api.base.routers import router
from api.base.views import (
    conference_watch_url,
    fakturownia_sale_recording_webhook,
    health_check,
    regon_autocomplete,
)

app_name = "api"  # pylint: disable=invalid-name

urlpatterns = [
    path("regon-autocomplete/", regon_autocomplete, name="regon-autocomplete"),
    path("health-check/", health_check, name="health-check"),
    path(
        "fakturownia-sale-recording-webhook/",
        fakturownia_sale_recording_webhook,
        name="fakturownia_sale_recording_webhook",
    ),
    path(
        "conference-watch-url/<uuid:uuid>/",
        conference_watch_url,
        name="conference-watch-url",
    ),
    path("", include(router.urls)),
]
