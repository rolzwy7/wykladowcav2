from django.urls import path

from core.views.crm.tagging import (
    crm_tag_single_email_page,
    crm_tagging_dashboard_page,
    crm_tagging_iframe_mirror,
    crm_tagging_import_emails_page,
    crm_tagging_paste_text_page,
    crm_tagging_tool,
)

urlpatterns = [
    path(
        "iframe-mirror/",
        crm_tagging_iframe_mirror,
        name="crm_tagging_iframe_mirror",
    ),
    path(
        "tool/",
        crm_tagging_tool,
        name="crm_tagging_tool",
    ),
    path(
        "taguj-email/",
        crm_tag_single_email_page,
        name="crm_tag_single_email_page",
    ),
    path(
        "wklej-tekst/",
        crm_tagging_paste_text_page,
        name="crm_tagging_paste_text_page",
    ),
    path(
        "importuj-emaile/<str:tag>/",
        crm_tagging_import_emails_page,
        name="crm_tagging_import_emails_page",
    ),
    path(
        "",
        crm_tagging_dashboard_page,
        name="crm_tagging_dashboard_page",
    ),
]
