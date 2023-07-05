from django.urls import include, path

from core.views import (
    home_page,
    login_page,
    register_page,
    webinar_category_page,
)
from core.views.lecturer import lecturer_list_page

from .application_urls import urlpatterns as application_urlpatterns
from .certificate_urls import urlpatterns as certificate_urlpatterns
from .crm_urls import urlpatterns as crm_urlpatterns
from .lecturer_urls import urlpatterns as lecturer_urlpatterns
from .previews_urls import urlpatterns as previews_urlpatterns
from .terms_and_conditions_urls import (
    urlpatterns as terms_and_conditions_urlpatterns,
)
from .webinar_urls import urlpatterns as webinar_urlpatterns

app_name = "core"

urlpatterns = [
    path(
        "szkolenia-<slug:slug>/",
        webinar_category_page,
        name="webinar_category_page",
    ),
    # path("api/", include("api.urls"), namespace="api"),
    path("zgloszenie-online/", include(application_urlpatterns)),
    path("szkolenie/", include(webinar_urlpatterns)),
    path("wykladowcy/", lecturer_list_page, name="lecturer_list_page"),
    path("wykladowca/", include(lecturer_urlpatterns)),
    path("crm/", include(crm_urlpatterns)),
    path("login/", login_page, name="login"),
    path("rejestracja/", register_page, name="register"),
    path("preview/", include(previews_urlpatterns)),
    path("certyfikat/", include(certificate_urlpatterns)),
    *terms_and_conditions_urlpatterns,
    path("", home_page, name="homepage"),
]
