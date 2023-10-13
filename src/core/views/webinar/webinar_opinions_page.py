from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar
from core.services import OpinionsService
from core.services.lecturer import LecturerService
from core.services.webinar import WebinarService


def webinar_opinions_page(request, slug: str):
    """Webinar page - opinions tab tab"""
    template_name = "geeks/pages/webinar/WebinarOpinionsPage.html"
    webinar = get_object_or_404(Webinar, slug=slug)
    webinar_service = WebinarService(webinar)
    lecturer_service = LecturerService(webinar.lecturer)
    opinions_service = OpinionsService(lecturer_service.get_lecturer_opinions())
    page_number = request.GET.get("strona")

    return TemplateResponse(
        request,
        template_name,
        {
            "webinar": webinar,
            "webinar_tabs": webinar_service.get_webinar_tabs(2),
            "lecturer_service": lecturer_service,
            "opinions_page": opinions_service.get_opinions_page(
                page_number, per_page=15
            ),
            "opinions_average": opinions_service.get_opinions_average(),
            "opinions_breakdown": opinions_service.get_opinions_breakdown(),
        },
    )
