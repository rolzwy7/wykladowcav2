from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar
from core.services.lecturer import LecturerService
from core.services.webinar import WebinarService


def webinar_program_page(request, slug: str):
    """Webinar program controller"""
    template_name = "geeks/pages/webinar/WebinarProgramPage.html"
    webinar = get_object_or_404(Webinar, slug=slug)
    webinar_service = WebinarService(webinar)
    lecturer_service = LecturerService(webinar.lecturer)

    return TemplateResponse(
        request,
        template_name,
        {
            "META__TITLE": webinar.title,
            "webinar": webinar,
            "related_webinars": webinar_service.get_related_webinars(),
            "webinar_tabs": webinar_service.get_webinar_tabs(0),
            "lecturer_service": lecturer_service,
        },
    )
