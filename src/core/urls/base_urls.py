from django.urls import include, path

from core.views import (
    home_page,
    lecturer_list_page,
    login_page,
    register_page,
    webinar_category_page,
)

from .application_urls import urlpatterns as application_urlpatterns
from .lecturer_urls import urlpatterns as lecturer_urlpatterns
from .webinar_urls import urlpatterns as webinar_urlpatterns

app_name = "core"

urlpatterns = [
    path("wykladowcy/", lecturer_list_page, name="lecturers"),
    path("login/", login_page, name="login"),
    path("rejestracja/", register_page, name="register"),
    path("zgloszenie-online/", include(application_urlpatterns)),
    path("szkolenie/", include(webinar_urlpatterns)),
    path("wykladowcy/", include(lecturer_urlpatterns)),
    path(
        "szkolenia-<slug:slug>/",
        webinar_category_page,
        name="webinar_category_page",
    ),
    path("api/", include("api.urls")),
    path("", home_page, name="homepage"),
]
