from django.urls import path

from core.views.leads import (
    lead_footer_post_endpoint,
    lead_webinar_post_endpoint,
    leads_thanks_page,
)

urlpatterns = [
    path(
        "zapisz-kontakt-stopka/",
        lead_footer_post_endpoint,
        name="lead_footer_post_endpoint",
    ),
    path(
        "zapisz-kontakt-archiwum-webinar/<int:pk>/",
        lead_webinar_post_endpoint,
        name="lead_webinar_post_endpoint",
    ),
    path(
        "dziekujemy/",
        leads_thanks_page,
        name="leads_thanks_page",
    ),
]
