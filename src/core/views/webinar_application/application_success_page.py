from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar, WebinarApplication


def application_success_page(request, uuid):
    """Application success page"""
    template_name = "geeks/pages/application/ApplicationSuccessPage.html"

    application = get_object_or_404(WebinarApplication, uuid=uuid)
    webinar: Webinar = application.webinar

    return TemplateResponse(
        request,
        template_name,
        {
            "webinar": webinar,
            "application": application,
        },
    )
