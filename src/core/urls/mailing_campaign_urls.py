from django.urls import path

from core.views.crm.mailing import (
    crm_mailing_campaign_add_emails,
    crm_mailing_campaign_delete_emails,
    crm_mailing_campaign_detail,
    crm_mailing_campaign_email_search_page,
    crm_mailing_campaign_list,
    crm_mailing_campaign_preview_html,
    crm_mailing_campaign_preview_text,
    crm_mailing_campaign_send_test_email,
)

urlpatterns = [
    path(
        "<int:pk>/",
        crm_mailing_campaign_detail,
        name="crm_mailing_campaign_detail",
    ),
    path(
        "<int:pk>/szukaj/",
        crm_mailing_campaign_email_search_page,
        name="crm_mailing_campaign_email_search_page",
    ),
    path(
        "<int:pk>/dodaj-emaile/",
        crm_mailing_campaign_add_emails,
        name="crm_mailing_campaign_add_emails",
    ),
    path(
        "<int:pk>/usun-emaile/",
        crm_mailing_campaign_delete_emails,
        name="crm_mailing_campaign_delete_emails",
    ),
    path(
        "<int:pk>/testowy-email/",
        crm_mailing_campaign_send_test_email,
        name="crm_mailing_campaign_send_test_email",
    ),
    path(
        "<int:pk>/podglad/html/",
        crm_mailing_campaign_preview_html,
        name="crm_mailing_campaign_preview_html",
    ),
    path(
        "<int:pk>/podglad/text/",
        crm_mailing_campaign_preview_text,
        name="crm_mailing_campaign_preview_text",
    ),
    path(
        "",
        crm_mailing_campaign_list,
        name="crm_mailing_campaigns_list",
    ),
]