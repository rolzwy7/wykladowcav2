from django.urls import path

from core.views.leads import lead_footer_post_endpoint, leads_thanks_page

urlpatterns = [
    path(
        "zapisz-kontakt/",
        lead_footer_post_endpoint,
        name="lead_footer_post_endpoint",
    ),
    path(
        "dziekujemy/",
        leads_thanks_page,
        name="leads_thanks_page",
    ),
]
