from django.urls import include, path

from htmx.views.contact_message import htmx_contact_message
from htmx.views.webinar_mailings import htmx_webinar_mailing_modal

from .application_urls import urlpatterns as application_urlpatterns
from .crm_urls import urlpatterns as crm_urlpatterns

app_name = "htmx"

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
    path("application/", include(application_urlpatterns)),
    path("crm/", include(crm_urlpatterns)),
]
