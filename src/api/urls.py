from django.urls import path

from api.base.views import regon_autocomplete

app_name = "api"

urlpatterns = [
    path("regon-autocomplete/", regon_autocomplete, name="regon-autocomplete")
]
