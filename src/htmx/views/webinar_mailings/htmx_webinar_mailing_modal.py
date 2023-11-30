from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import MailingCampaign, Webinar


def htmx_webinar_mailing_modal(request: HttpRequest, pk: int):
    """htmx_webinar_mailing_modal"""
    template_path = "htmx/htmx_webinar_mailing_modal.html"
    webinar = get_object_or_404(Webinar, pk=pk)
    campaigns = MailingCampaign.manager.filter(webinar=webinar)

    return TemplateResponse(
        request,
        template_path,
        {"webinar": webinar, "campaigns": campaigns},
    )
