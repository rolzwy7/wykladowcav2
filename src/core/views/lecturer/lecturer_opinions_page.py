from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Lecturer
from core.services.lecturer_service import LecturerService


def lecturer_opinions_page(request, slug: str):
    """List of lecturers"""
    template_name = "core/pages/lecturer/LecturerOpinionsPage.html"
    lecturer = get_object_or_404(Lecturer, slug=slug)
    service = LecturerService(lecturer)

    return TemplateResponse(
        request,
        template_name,
        {
            "lecturer": lecturer,
            "tabs": service.get_lecturer_tabs(2),
            "opinions": service.get_lecturer_opinions(),
            "opinions_sequence": [1, 2, 3, 4, 5],
        },
    )
