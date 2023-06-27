from django.urls import path

from core.views.crm import crm_upcoming_webinars, crm_webinar_detail_dashboard

urlpatterns = [
    path(
        "webinar/<int:pk>/",
        crm_webinar_detail_dashboard,
        name="crm_webinar_detail_dashboard",
    ),
    path(
        "",
        crm_upcoming_webinars,
        name="crm_upcoming_webinars",
    ),
]
