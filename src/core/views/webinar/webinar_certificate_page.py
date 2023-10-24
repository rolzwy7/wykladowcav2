from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar
from core.services.lecturer import LecturerService
from core.services.webinar import WebinarService


def webinar_certificate_page(request, slug: str):
    """Webinar page - price and invoice tab"""
    template_name = "geeks/pages/webinar/WebinarCertificatePage.html"
    webinar = get_object_or_404(Webinar, slug=slug)
    webinar_service = WebinarService(webinar)
    lecturer_service = LecturerService(webinar.lecturer)

    return TemplateResponse(
        request,
        template_name,
        {
            "webinar": webinar,
            "related_webinars": webinar_service.get_related_webinars(),
            "webinar_tabs": webinar_service.get_webinar_tabs(3),
            "lecturer_service": lecturer_service,
        },
    )
