from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar
from core.services.lecturer import LecturerService
from core.services.webinar import WebinarService


def webinar_faq_page(request, slug: str):
    """Webinar page - faq tab"""
    template_name = "geeks/pages/webinar/WebinarFaqPage.html"
    webinar = get_object_or_404(Webinar, slug=slug)
    webinar_service = WebinarService(webinar)
    lecturer_service = LecturerService(webinar.lecturer)

    return TemplateResponse(
        request,
        template_name,
        {
            "webinar": webinar,
            "webinar_tabs": webinar_service.get_webinar_tabs(4),
            "lecturer_service": lecturer_service,
        },
    )
