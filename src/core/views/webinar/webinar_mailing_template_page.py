from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar
from core.services import MailingWebinarTemplateService


def webinar_mailing_template_page(request: HttpRequest, pk: int):
    """Webinar email template page"""
    template_name = "core/pages/webinar/mailing/WebinarMailingBase.html"
    webinar = get_object_or_404(Webinar, pk=pk)
    service = MailingWebinarTemplateService(webinar)

    return TemplateResponse(
        request,
        template_name,
        {"webinar": webinar, **service.get_context()},
    )
