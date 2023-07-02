from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Lecturer
from core.services.lecturer_service import LecturerService


def lecturer_webinars_page(request, slug: str):
    """List of lecturer's webinars"""
    template_name = "core/pages/lecturer/LecturerWebinarsPage.html"
    lecturer = get_object_or_404(Lecturer, slug=slug)
    service = LecturerService(lecturer)

    return TemplateResponse(
        request,
        template_name,
        {
            "lecturer": lecturer,
            "tabs": service.get_lecturer_tabs(1),
            "webinars": service.get_lecturer_webinars(),
        },
    )
