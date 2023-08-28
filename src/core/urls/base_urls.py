from django.urls import include, path

from core.views import (
    about_us_page,
    contact_page,
    home_page,
    login_page,
    logout_page,
    webinar_category_page,
)
from core.views.lecturer import lecturer_list_page
from core.views.mailing_resignation import mailing_resignation_page

from .application_urls import urlpatterns as application_urlpatterns
from .assets_urls import urlpatterns as assets_urlpatterns
from .certificate_urls import urlpatterns as certificate_urlpatterns
from .crm_urls import urlpatterns as crm_urlpatterns
from .lecturer_urls import urlpatterns as lecturer_urlpatterns
from .loyalty_urls import urlpatterns as loyalty_urlpatterns
from .previews_urls import urlpatterns as previews_urlpatterns
from .recording_urls import urlpatterns as recording_urlpatterns
from .registration_urls import urlpatterns as registration_urlpatterns
from .terms_and_conditions_urls import (
    urlpatterns as terms_and_conditions_urlpatterns,
)
from .webinar_urls import urlpatterns as webinar_urlpatterns

app_name = "core"

urlpatterns = [
    path(
        "szkolenia/<slug:slug>/",
        webinar_category_page,
        name="webinar_category_page",
    ),
    # path("api/", include("api.urls"), namespace="api"),
    path("program-partnerski/", include(loyalty_urlpatterns)),
    path("zgloszenie-online/", include(application_urlpatterns)),
    path("szkolenia-online/", include(webinar_urlpatterns)),
    path("rejestracja/", include(registration_urlpatterns)),
    path("wykladowcy/", lecturer_list_page, name="lecturer_list_page"),
    path("wykladowca/", include(lecturer_urlpatterns)),
    path("crm/", include(crm_urlpatterns)),
    path("logowanie/", login_page, name="login_page"),
    path("wyloguj/", logout_page, name="logout_page"),
    path("kontakt/", contact_page, name="contact_page"),
    path("o-nas/", about_us_page, name="about_us_page"),
    path("preview/", include(previews_urlpatterns)),
    path("certyfikat/", include(certificate_urlpatterns)),
    path("nagrania/", include(recording_urlpatterns)),
    path("materialy-szkoleniowe/", include(assets_urlpatterns)),
    path(
        "rezygnacja/<str:resignation_code>/",
        mailing_resignation_page,
        name="mailing_resignation_page",
    ),
    *terms_and_conditions_urlpatterns,
    path("", home_page, name="homepage"),
]
