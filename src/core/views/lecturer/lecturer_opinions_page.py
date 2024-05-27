"""Lecturers opinions list page"""

from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Lecturer
from core.services import OpinionsService
from core.services.lecturer import LecturerService


def lecturer_opinions_page(request, slug: str):
    """List of lecturers"""
    template_name = "geeks/pages/lecturer/LecturerOpinionsPage.html"
    lecturer = get_object_or_404(Lecturer, slug=slug)
    lecturer_service = LecturerService(lecturer)

    opinions_service = OpinionsService(lecturer_service.get_lecturer_opinions())
    page_number = request.GET.get("strona")

    return TemplateResponse(
        request,
        template_name,
        {
            "lecturer": lecturer,
            "opinions_page": opinions_service.get_opinions_page(
                page_number, per_page=15
            ),
            "opinions_average": opinions_service.get_opinions_average(),
            "opinions_breakdown": opinions_service.get_opinions_breakdown(),
        },
    )
