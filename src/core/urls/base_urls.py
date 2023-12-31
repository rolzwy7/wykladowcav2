"""
Base URLs
"""
# flake8: noqa:E501
# pylint: disable=line-too-long
from django.urls import include, path
from django.views.generic.base import RedirectView

from core.views import (
    about_us_page,
    contact_page,
    home_page,
    login_page,
    logout_page,
    webmap_page,
)
from core.views.custom_error_pages import custom404_page, custom500_page
from core.views.lecturer import lecturer_list_page
from core.views.mailing_resignation import (
    mailing_resignation_by_code_page,
    mailing_resignation_by_form_page,
)

from .application_urls import urlpatterns as application_urlpatterns
from .assets_urls import urlpatterns as assets_urlpatterns
from .category_urls import urlpatterns as category_urlpatterns
from .certificate_urls import urlpatterns as certificate_urlpatterns
from .conference_urls import urlpatterns as conference_urlpatterns
from .crm_urls import urlpatterns as crm_urlpatterns
from .forgot_password_urls import urlpatterns as forgot_password_urlpatterns
from .leads_urls import urlpatterns as leads_urlpatterns
from .lecturer_urls import urlpatterns as lecturer_urlpatterns
from .loyalty_urls import urlpatterns as loyalty_urlpatterns
from .mailing_templates_urls import urlpatterns as mailing_templates_urlpatterns
from .previews_urls import urlpatterns as previews_urlpatterns
from .recording_urls import urlpatterns as recording_urlpatterns
from .registration_urls import urlpatterns as registration_urlpatterns
from .terms_and_conditions_urls import urlpatterns as terms_and_conditions_urlpatterns
from .user_account_urls import urlpatterns as user_account_urlpatterns
from .webinar_urls import urlpatterns as webinar_urlpatterns

app_name = "core"  # pylint: disable=invalid-name

urlpatterns = [
    # path("api/", include("api.urls"), namespace="api"),
    path("szkolenia-online/", include(webinar_urlpatterns)),
    path("szkolenia/", include(category_urlpatterns)),
    path("polecaj-i-zarabiaj/", include(loyalty_urlpatterns)),
    path("zgloszenie-online/", include(application_urlpatterns)),
    path("przypomnij-haslo/", include(forgot_password_urlpatterns)),
    path("rejestracja/", include(registration_urlpatterns)),
    path("wykladowcy/", lecturer_list_page, name="all_lecturers_list_page"),
    path("wykladowca/", include(lecturer_urlpatterns)),
    path("crm/", include(crm_urlpatterns)),
    path("logowanie/", login_page, name="login_page"),
    path("wyloguj/", logout_page, name="logout_page"),
    path("kontakt/", contact_page, name="contact_page"),
    path("o-nas/", about_us_page, name="about_us_page"),
    path("mapa-strony/", webmap_page, name="webmap_page"),
    path("preview/", include(previews_urlpatterns)),
    path("certyfikat/", include(certificate_urlpatterns)),
    path("nagrania/", include(recording_urlpatterns)),
    path("materialy-szkoleniowe/", include(assets_urlpatterns)),
    path("leads/", include(leads_urlpatterns)),
    path(
        "rezyg/formularz/",
        mailing_resignation_by_form_page,
        name="mailing_resignation_by_form_page",
    ),
    path(
        "rezyg/<str:resignation_code>/",
        mailing_resignation_by_code_page,
        name="mailing_resignation_page",
    ),
    path("szablony-mailingowe/", include(mailing_templates_urlpatterns)),
    path("moje-konto/", include(user_account_urlpatterns)),
    *terms_and_conditions_urlpatterns,
    #
    path(
        "r/pp",
        RedirectView.as_view(url="/polecaj-i-zarabiaj/informacje/"),
        name="redirect_loyalty_program",
    ),
    # Test error pages
    path("404/", custom404_page, name="custom404_page"),
    path("500/", custom500_page, name="custom500_page"),
    #
    path("szkolenia-cykliczne/", include(conference_urlpatterns)),
    path("", home_page, name="homepage"),
]
