from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Lecturer
from core.services.lecturer import LecturerService


def lecturer_closed_webinar_pages(request, slug: str):
    """Lecturer closed webinar page"""
    template_name = "geeks/pages/lecturer/LecturerClosedWebinarPages.html"
    lecturer = get_object_or_404(Lecturer, slug=slug)
    if lecturer.finished_coop:
        raise Http404("Zakończono współpracę")

    service = LecturerService(lecturer)

    return TemplateResponse(
        request,
        template_name,
        {"lecturer": lecturer, "tabs": service.get_lecturer_tabs(0)},
    )
