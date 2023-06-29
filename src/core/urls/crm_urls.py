from django.urls import path

from core.views.crm import (
    crm_upcoming_webinars,
    crm_webinar_confirm,
    crm_webinar_detail_dashboard,
    crm_webinar_eventlogs,
)

urlpatterns = [
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
        "webinar/<int:pk>/potwierdz-termin/",
        crm_webinar_confirm,
        name="crm_webinar_confirm",
    ),
    path(
        "",
        crm_upcoming_webinars,
        name="crm_upcoming_webinars",
    ),
]
