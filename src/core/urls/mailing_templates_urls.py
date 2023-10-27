# flake8: noqa:E501
# pylint: disable=line-too-long

from django.urls import path
from django.views.generic import TemplateView

from core.views.webinar import webinar_mailing_template_page

urlpatterns = [
    # Facebook
    path(
        "fb-group-invite-version-a/",
        TemplateView.as_view(
            template_name="mailing_templates/MailingFacebookGroupInvite/VersionA.html"
        ),
        name="mailing-template-fb-group-invite",
    ),
    # Webinar Mailing Template
    path(
        "<int:pk>/szablon-mailingowy/<str:template_name>/",
        webinar_mailing_template_page,
        name="webinar_mailing_template_page",
    ),
]
