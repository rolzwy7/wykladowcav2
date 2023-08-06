from django.urls import path

from core.views.crm import (
    crm_archived_webinars,
    crm_eventlogs,
    crm_todos_done_list,
    crm_todos_list,
    crm_upcoming_webinars,
    crm_webinar_assets,
    crm_webinar_certificates,
    crm_webinar_detail_dashboard,
    crm_webinar_eventlogs,
    crm_webinar_invoices,
    crm_webinar_recordings,
)
from core.views.crm.company import CrmCompanyDetail, CrmCompanyList
from core.views.crm.contact import CrmContactDetail, CrmContactList
from core.views.crm.mailing import (
    crm_mailing_campaign_add_emails,
    crm_mailing_campaign_delete_emails,
    crm_mailing_campaign_detail,
    crm_mailing_campaign_list,
)
from core.views.crm.webinar.actions import (
    CancelWebinarAction,
    ConfirmWebinarAction,
    DoneWebinarAction,
    move_webinar_action,
)

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
    # Mailing TODO: move this to seperate urlpatterns
    path(
        "kampanie-mailingowe/",
        crm_mailing_campaign_list,
        name="crm_mailing_campaigns_list",
    ),
    path(
        "kampanie-mailingowe/<int:pk>/",
        crm_mailing_campaign_detail,
        name="crm_mailing_campaign_detail",
    ),
    path(
        "kampanie-mailingowe/<int:pk>/dodaj-emaile/",
        crm_mailing_campaign_add_emails,
        name="crm_mailing_campaign_add_emails",
    ),
    path(
        "kampanie-mailingowe/<int:pk>/usun-emaile/",
        crm_mailing_campaign_delete_emails,
        name="crm_mailing_campaign_delete_emails",
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
        "logi/",
        crm_eventlogs,
        name="crm_eventlogs",
    ),
    path(
        "",
        crm_upcoming_webinars,
        name="crm_upcoming_webinars",
    ),
]
