"""HTMX URLs"""

# flake8: noqa=E501

from django.urls import include, path

from htmx.views.contact_message import htmx_contact_message
from htmx.views.static_files import disc_space
from htmx.views.tracking.tracking_mailing import tracking_mailing
from htmx.views.webinar_mailings import htmx_webinar_mailing_modal
from htmx.views.webinar_omega_indexer import webinar_omega_indexer

from .application_urls import urlpatterns as application_urlpatterns
from .crm_urls import urlpatterns as crm_urlpatterns

app_name = "htmx"  # pylint: disable=invalid-name

urlpatterns = [
    path(
        "webinar-mailing-modal/<int:pk>/",
        htmx_webinar_mailing_modal,
        name="htmx_webinar_mailing_modal",
    ),
    path(
        "contact_message",
        htmx_contact_message,
        name="htmx_contact_message",
    ),
    path(
        "webinar-omega-indexer/<int:pk>/",
        webinar_omega_indexer,
        name="webinar-omega-indexer",
    ),
    path(
        "static-files/disc-space/",
        disc_space,
        name="static-files-disc-space",
    ),
    path(
        "tracking_mailing/<str:tracking_code>/",
        tracking_mailing,
        name="tracking_mailing",
    ),
    path(
        "crm/lecturer-price/",
        include("htmx.views.lecturer_price.urls", namespace="lecturer-price"),
    ),
    path(
        "system-health/",
        include("htmx.views.system_health.urls", namespace="system-health"),
    ),
    path(
        "dwpldb/",
        include("htmx.views.dwpldb.urls", namespace="dwpldb"),
    ),
    path("application/", include(application_urlpatterns)),
    path("crm/", include(crm_urlpatterns)),
]
