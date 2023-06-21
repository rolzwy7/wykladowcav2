from django.urls import include, path

from core.views import home_page, lecturer_list_page, login_page, register_page

from .application_urls import urlpatterns as application_urlpatterns
from .lecturer_urls import urlpatterns as lecturer_urlpatterns
from .webinar_categories_urls import (
    urlpatterns as webinar_categories_urlpatterns,
)
from .webinar_urls import urlpatterns as webinar_urlpatterns

app_name = "core"

urlpatterns = [
    path("wykladowcy/", lecturer_list_page, name="lecturers"),
    path("login/", login_page, name="login"),
    path("rejestracja/", register_page, name="register"),
    path("zgloszenie-online/", include(application_urlpatterns)),
    path("szkolenie/", include(webinar_urlpatterns)),
    path("wykladowcy/", include(lecturer_urlpatterns)),
    path("kategoria/", include(webinar_categories_urlpatterns)),
    path("", home_page, name="homepage"),
]
