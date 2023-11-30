# flake8: noqa:E501
# pylint: disable=line-too-long
from django.urls import include, path

from core.views.crm import (
    crm_archived_webinars,
    crm_blacklist_paste,
    crm_contact_messages,
    crm_eventlogs,
    crm_resignations_plaintext,
    crm_take_over_account,
    crm_todos_done_list,
    crm_todos_list,
    crm_upcoming_webinars,
    crm_webinar_assets,
    crm_webinar_certificates,
    crm_webinar_detail_dashboard,
    crm_webinar_duplicate,
    crm_webinar_eventlogs,
    crm_webinar_export_participants,
    crm_webinar_invoices,
    crm_webinar_recordings,
)
from core.views.crm.company import CrmCompanyDetail, CrmCompanyList
from core.views.crm.contact import CrmContactDetail, CrmContactList
from core.views.crm.mailing import download_emails_from_sender_page
from core.views.crm.recording import crm_send_recording_to_all_participants
from core.views.crm.statistics import crm_statistics_dashboard
from core.views.crm.webinar.actions import (
    CancelWebinarAction,
    ConfirmWebinarAction,
    DoneWebinarAction,
    move_webinar_action,
)

from .lecturer_urls import urlpatterns as lecturer_urlpatterns
from .mailing_campaign_urls import urlpatterns as mailing_campaign_urlpatterns
from .tagging_url import urlpatterns as tagging_urlpatterns

urlpatterns = [
    # Webinar
    path(
        "webinar/<int:pk>/",
        crm_webinar_detail_dashboard,
        name="crm_webinar_detail_dashboard",
    ),
    path(
        "webinar/<int:pk>/logi/",
        crm_webinar_eventlogs,
        name="crm_webinar_eventlogs",
    ),
    path(
        "webinar/<int:pk>/eksportuj-uczestnikow/",
        crm_webinar_export_participants,
        name="crm_webinar_export_participants",
    ),
    path(
        "webinar/<int:pk>/duplikuj-szkolenie/",
        crm_webinar_duplicate,
        name="crm_webinar_duplicate",
    ),
    path(
        "webinar/<int:pk>/faktury/",
        crm_webinar_invoices,
        name="crm_webinar_invoices",
    ),
    path(
        "webinar/<int:pk>/materialy-szkoleniowe/",
        crm_webinar_assets,
        name="crm_webinar_assets",
    ),
    path(
        "webinar/<int:pk>/nagrania/",
        crm_webinar_recordings,
        name="crm_webinar_recordings",
    ),
    path(
        "webinar/<int:pk>/certyfikaty/",
        crm_webinar_certificates,
        name="crm_webinar_certificates",
    ),
    path(
        "webinar/<int:pk>/potwierdz-termin/",
        ConfirmWebinarAction.as_view(),
        name="crm_webinar_confirm",
    ),
    path(
        "webinar/<int:pk>/odwolaj-termin/",
        CancelWebinarAction.as_view(),
        name="crm_webinar_cancel",
    ),
    path(
        "webinar/<int:pk>/zakoncz-termin/",
        DoneWebinarAction.as_view(),
        name="crm_webinar_done",
    ),
    path(
        "webinar/<int:pk>/przenies/",
        move_webinar_action,
        name="crm_webinar_move",
    ),
    # CRM company
    path(
        "firmy/",
        CrmCompanyList.as_view(),
        name="crm_company_list",
    ),
    path(
        "firmy/<int:pk>/",
        CrmCompanyDetail.as_view(),
        name="crm_company_detail",
    ),
    # CRM contact
    path(
        "kontaky/",
        CrmContactList.as_view(),
        name="crm_contact_list",
    ),
    path(
        "kontaky/<int:pk>/",
        CrmContactDetail.as_view(),
        name="crm_contact_detail",
    ),
    # Archive
    path(
        "archiwum/",
        crm_archived_webinars,
        name="crm_archived_webinars",
    ),
    path(
        "pobierz-emaile-konto-wysylkowe/<int:pk>/<str:export_type>/",
        download_emails_from_sender_page,
        name="download_emails_from_sender_page",
    ),
    path("kampanie-mailingowe/", include(mailing_campaign_urlpatterns)),
    path("tagowanie/", include(tagging_urlpatterns)),
    path("wykladowcy/", include(lecturer_urlpatterns)),
    # Take over account
    path(
        "przejmij-konto/",
        crm_take_over_account,
        name="crm_take_over_account",
    ),
    # Blacklist paste
    path(
        "czarna-lista/",
        crm_blacklist_paste,
        name="crm_blacklist_paste",
    ),
    path(
        "rezygnacje/",
        crm_resignations_plaintext,
        name="crm_resignations_plaintext",
    ),
    # Tasks
    path(
        "zadania/wykonane/",
        crm_todos_done_list,
        name="crm_todos_done_list",
    ),
    path(
        "zadania/",
        crm_todos_list,
        name="crm_todos_list",
    ),
    path(
        "pytania/",
        crm_contact_messages,
        name="crm_contact_messages",
    ),
    path(
        "logi/",
        crm_eventlogs,
        name="crm_eventlogs",
    ),
    # Recordings
    path(
        "nagrania/<str:recording_id>/wyslij-wszystkim-uczestnikom/",
        crm_send_recording_to_all_participants,
        name="crm_send_recordings_to_all_participants",
    ),
    # Statistics
    path(
        "statystyki/",
        crm_statistics_dashboard,
        name="crm_statistics_dashboard",
    ),
    # Upcoming webinars
    path(
        "",
        crm_upcoming_webinars,
        name="crm_upcoming_webinars",
    ),
]
