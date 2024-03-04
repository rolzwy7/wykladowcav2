"""API urls"""

from django.urls import include, path

from api.base.routers import router
from api.base.views import health_check, regon_autocomplete

app_name = "api"  # pylint: disable=invalid-name

urlpatterns = [
    path("regon-autocomplete/", regon_autocomplete, name="regon-autocomplete"),
    path("health-check/", health_check, name="health-check"),
    path("", include(router.urls)),
]
