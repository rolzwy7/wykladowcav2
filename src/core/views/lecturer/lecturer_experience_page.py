"""Lecturer experience page"""

# flake8: noqa

from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Lecturer
from core.services import OpinionsService
from core.services.lecturer import LecturerService


def lecturer_experience_page(request, slug: str):
    """List of lecturers"""
    template_name = "geeks/pages/lecturer/LecturerExperiencePage.html"
    lecturer = get_object_or_404(Lecturer, slug=slug)

    lecturer_service = LecturerService(lecturer)
    lecturer_opinions = lecturer_service.get_lecturer_opinions()
    opinions_service = OpinionsService(lecturer_opinions)
    page_number = request.GET.get("strona")

    return TemplateResponse(
        request,
        template_name,
        {
            "lecturer": lecturer,
            "tabs": lecturer_service.get_lecturer_tabs(0),
            "webinars": lecturer_service.get_lecturer_webinars(),
            "nearest_webinar": lecturer_service.get_lecturer_nearest_webinar(),
            "hide_footer_newsletter_singup": True,
            "opinions_page": opinions_service.get_opinions_page(
                page_number, per_page=15
            ),
            "opinions_average": opinions_service.get_opinions_average(),
            "opinions_breakdown": opinions_service.get_opinions_breakdown(),
            "opinions_count": lecturer_opinions.count(),
            "main_opinions": lecturer_service.get_lecturer_main_opinions(),
        },
    )
