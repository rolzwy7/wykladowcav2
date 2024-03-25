"""HTMX URLs"""

# flake8: noqa=E501

from django.urls import include, path

from htmx.views.contact_message import htmx_contact_message
from htmx.views.tracking.tracking_mailing import tracking_mailing
from htmx.views.webinar_mailings import htmx_webinar_mailing_modal

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
    path("application/", include(application_urlpatterns)),
    path("crm/", include(crm_urlpatterns)),
]
