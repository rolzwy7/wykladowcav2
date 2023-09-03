from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Lecturer
from core.services.lecturer import LecturerService


def lecturer_experience_page(request, slug: str):
    """List of lecturers"""
    template_name = "geeks/pages/lecturer/LecturerExperiencePage.html"
    lecturer = get_object_or_404(Lecturer, slug=slug)
    service = LecturerService(lecturer)

    return TemplateResponse(
        request,
        template_name,
        {"lecturer": lecturer, "tabs": service.get_lecturer_tabs(0)},
    )
