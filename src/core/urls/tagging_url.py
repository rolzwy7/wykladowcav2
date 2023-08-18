from django.urls import path

from core.views.crm.tagging import (
    crm_tagging_dashboard_page,
    crm_tagging_iframe_mirror,
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
        "",
        crm_tagging_dashboard_page,
        name="crm_tagging_dashboard_page",
    ),
]
