# flake8: noqa:E501
# pylint: disable=line-too-long

from django.urls import path
from django.views.generic import TemplateView

from core.views.editor_email_page import editor_email_page
from core.views.webinar import webinar_mailing_template_page

urlpatterns = [
    path("<int:pk>/edytor-mailingowy/", editor_email_page, name="editor_email_page"),
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
        "<int:pk>/szablon-mailingowy/",
        webinar_mailing_template_page,
        name="webinar_mailing_template_page",
    ),
]
