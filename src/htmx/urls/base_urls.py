from django.urls import include, path

from .application_urls import urlpatterns as application_urlpatterns
from .crm_urls import urlpatterns as crm_urlpatterns

app_name = "htmx"

urlpatterns = [
    path("application/", include(application_urlpatterns)),
    path("crm/", include(crm_urlpatterns)),
]
