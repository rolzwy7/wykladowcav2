# flake8: noqa:E501
# pylint: disable=line-too-long

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar
from core.services.mailing import MailingWebinarTemplateService
from core.services.webinar import WebinarService


def webinar_mailing_template_page(request: HttpRequest, pk: int):
    """Webinar email template page"""

    version = request.GET.get("version")
    webinar_for = request.GET.get("webinar_for")
    patron_section = request.GET.get("patron_section")
    lecturer_section = request.GET.get("lecturer_section")
    promo_code = request.GET.get("promo_code")
    promo_text = request.GET.get("promo_text")
    promo_value = request.GET.get("promo_value")
    section_loyalty = request.GET.get("section_loyalty")
    section_fb_kk_job = request.GET.get("section_fb_kk_job")
    show_last_spots = request.GET.get("show_last_spots")
    show_price = request.GET.get("show_price")
    show_logo = request.GET.get("show_logo")

    template_name = f"mailing_templates/MailingTemplateWebinarOffer/{version}.html"
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
            "webinar_for": webinar_for,
            "patron_section": patron_section,
            "lecturer_section": lecturer_section,
            "promo_code": promo_code,
            "promo_text": promo_text,
            "promo_value": promo_value,
            "section_loyalty": section_loyalty,
            "section_fb_kk_job": section_fb_kk_job,
            "show_last_spots": show_last_spots,
            "show_price": show_price,
            "show_logo": show_logo,
        },
    )
