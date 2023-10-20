from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar
from core.services.mailing import MailingWebinarTemplateService
from core.services.webinar import WebinarService


def webinar_mailing_template_page(
    request: HttpRequest, pk: int, template_name: str
):
    """Webinar email template page"""
    template_name = (
        f"mailing_templates/MailingTemplateWebinarOffer/{template_name}.html"
    )
    webinar = get_object_or_404(Webinar, pk=pk)
    webinar_template_service = MailingWebinarTemplateService(webinar)
    webinar_service = WebinarService(webinar)

    return TemplateResponse(
        request,
        template_name,
        {
            **webinar_template_service.get_context(),
            "webinar": webinar,
            "related_webinars": webinar_service.get_related_webinars(),
        },
    )
