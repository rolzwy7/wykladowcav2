# flake8: noqa:E501
# pylint: disable=line-too-long
from django.urls import include, path

from core.views.crm import (
    conference_from_webinar,
    confirm_free_participants,
    crm_aggregates_page,
    crm_aggregates_webinar_list_page,
    crm_ai_konsensus,
    crm_ai_page,
    crm_blacklist_paste,
    crm_clickmeeting_paste_stream,
    crm_contact_messages,
    crm_eventlogs,
    crm_invoices_list,
    crm_program_text_manual_adjust,
    crm_redirect,
    crm_resignations_plaintext,
    crm_send_webinar_queue_email_notifications,
    crm_take_over_account,
    crm_todos_done_list,
    crm_todos_list,
    crm_upcoming_webinars,
    crm_url_to_program,
    crm_user_password_reset,
    crm_users_page,
    crm_webinar_analysis,
    crm_webinar_assets,
    crm_webinar_bulk_duplicate,
    crm_webinar_certificates,
    crm_webinar_detail_dashboard,
    crm_webinar_duplicate,
    crm_webinar_eventlogs,
    crm_webinar_export_participants,
    crm_webinar_free_participants,
    crm_webinar_invoices,
    crm_webinar_new_from_url,
    crm_webinar_recordings,
    crm_word_to_program_text,
)
from core.views.crm.application.actions import (
    crm_application_resend_confirmation,
    crm_application_send_invoice_action_page,
    crm_free_participant_resend_confirmation,
)
from core.views.crm.company import CrmCompanyDetail, CrmCompanyList
from core.views.crm.contact import CrmContactDetail, CrmContactList
from core.views.crm.crm_archived_webinars import (
    crm_archived_webinars,
    crm_archived_webinars_with_applications,
)
from core.views.crm.crm_closed_webinars import crm_closed_webinars
from core.views.crm.inbox import crm_inbox_message_page, crm_inbox_page
from core.views.crm.mailing import download_emails_from_sender_page
from core.views.crm.recording import crm_send_recording_to_all_participants
from core.views.crm.seo import seo_graph_page
from core.views.crm.service_offer import service_offer_applications_list_page
from core.views.crm.sms import crm_send_sms
from core.views.crm.statistics import crm_statistics_dashboard
from core.views.crm.webinar.actions import (
    CancelWebinarAction,
    ConfirmWebinarAction,
    WebinarSendOpinionRequestsAction,
    crm_webinar_done_action_page,
    move_webinar_action,
)

from .lecturer_urls import urlpatterns as lecturer_urlpatterns
from .mailing_campaign_urls import urlpatterns as mailing_campaign_urlpatterns
from .tagging_url import urlpatterns as tagging_urlpatterns

urlpatterns = [
    path(
        "zapytania-szkolenia-zamkniete/",
        crm_closed_webinars,
        name="crm_closed_webinars",
    ),
    # Service Offer
    path(
        "uslugi-zgloszenia/",
        service_offer_applications_list_page,
        name="service_offer_applications_list_page",
    ),
    #
    path(
        "skrzynka-odbiorcza/wiadomosc/<str:email_id>",
        crm_inbox_message_page,
        name="crm_inbox_message_page",
    ),
    path(
        "skrzynka-odbiorcza/",
        crm_inbox_page,
        name="crm_inbox_page",
    ),
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
        "webinar/<int:pk>/darmowi-uczestnicy/",
        crm_webinar_free_participants,
        name="crm_webinar_free_participants",
    ),
    path(
        "webinar/<int:pk>/analiza/",
        crm_webinar_analysis,
        name="crm_webinar_analysis",
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
        "webinar/<int:pk>/clickmeeting-paste-stream-redirect/",
        crm_clickmeeting_paste_stream,
        name="crm_clickmeeting_paste_stream",
    ),
    path(
        "webinar/<int:pk>/word-to-program-text/",
        crm_word_to_program_text,
        name="crm_word_to_program_text",
    ),
    path(
        "webinar/<int:pk>/url-to-program/",
        crm_url_to_program,
        name="crm_url_to_program",
    ),
    path(
        "webinar/new-from-url/",
        crm_webinar_new_from_url,
        name="crm_webinar_new_from_url",
    ),
    path(
        "webinar/<int:pk>/program-text-manual-adjust/",
        crm_program_text_manual_adjust,
        name="crm_program_text_manual_adjust",
    ),
    path(
        "webinar/<int:pk>/bulk-duplicate/",
        crm_webinar_bulk_duplicate,
        name="crm_webinar_bulk_duplicate",
    ),
    # CRM Webinar Actions
    path(
        "zgloszenie/<int:pk>/przeslij-fakture/",
        crm_application_send_invoice_action_page,
        name="crm_application_send_invoice_action",
    ),
    path(
        "zgloszenie/<int:pk>/przeslij-ponownie-potwierdzenie/",
        crm_application_resend_confirmation,
        name="crm_application_resend_confirmation_action",
    ),
    # CRM Webinar Actions
    path(
        "webinar/<int:pk>/przeslij-prosby-o-opinie/",
        WebinarSendOpinionRequestsAction.as_view(),
        name="crm_webinar_send_opinion_request_action",
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
        crm_webinar_done_action_page,
        name="crm_webinar_done_action",
    ),
    path(
        "webinar/<int:pk>/przenies/",
        move_webinar_action,
        name="crm_webinar_move",
    ),
    path(
        "webinar/<int:pk>/stworz-konferencje-z-webinaru/",
        conference_from_webinar,
        name="conference_from_webinar",
    ),
    path(
        "webinar/<int:pk>/wyslij-przypomnienia-darmowym/",
        confirm_free_participants,
        name="confirm_free_participants",
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
        "archiwum-odwolane-ze-zgloszeniami/",
        crm_archived_webinars_with_applications,
        name="crm_archived_webinars_with_applications",
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
        "faktury/",
        crm_invoices_list,
        name="crm_invoices_list",
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
    # Konferencje
    path(
        "konferencja/darmowi-uczestnicy/<int:pk>/przeslij-ponownie-potwierdzenie/",
        crm_free_participant_resend_confirmation,
        name="crm_free_participant_resend_confirmation",
    ),
    # SMS
    path(
        "wyslij-sms/",
        crm_send_sms,
        name="crm_send_sms",
    ),
    # SEO
    path(
        "seo/graf/",
        seo_graph_page,
        name="seo_graph_page",
    ),
    # CRM Aggregates
    path(
        "agregaty/",
        crm_aggregates_page,
        name="crm_aggregates_page",
    ),
    # CRM Aggregates
    path(
        "agregaty/spis-terminow/",
        crm_aggregates_webinar_list_page,
        name="crm_aggregates_webinar_list_page",
    ),
    # CRM Users
    path(
        "uzytkownicy/",
        crm_users_page,
        name="crm_users_page",
    ),
    # User password reset
    path(
        "user-password-reset/<int:pk>/",
        crm_user_password_reset,
        name="crm_user_password_reset",
    ),
    #
    path(
        "send-webinar-queue-email-notifications/<str:grouping_token>/",
        crm_send_webinar_queue_email_notifications,
        name="crm_send_webinar_queue_email_notifications",
    ),
    path(
        "crm-redirect/<str:name>/<str:param>/",
        crm_redirect,
        name="crm_redirect",
    ),
    path(
        "ai/",
        crm_ai_page,
        name="crm_ai_page",
    ),
    path(
        "ai/agent.txt",
        crm_ai_konsensus,
        name="crm_ai_konsensus",
    ),
    # Upcoming webinars
    path(
        "",
        crm_upcoming_webinars,
        name="crm_upcoming_webinars",
    ),
]
