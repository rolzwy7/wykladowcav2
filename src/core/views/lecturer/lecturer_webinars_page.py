# flake8: noqa=E501

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Lecturer
from core.services.lecturer import LecturerService


def lecturer_webinars_page(request, slug: str):
    """List of lecturer's webinars"""
    template_name = "geeks/pages/lecturer/LecturerWebinarsPage.html"
    lecturer = get_object_or_404(Lecturer, slug=slug)
    if lecturer.finished_coop:
        raise Http404("Zakończono współpracę")

    lecturer_service = LecturerService(lecturer)

    return TemplateResponse(
        request,
        template_name,
        {
            "lecturer": lecturer,
            "tabs": lecturer_service.get_lecturer_tabs(1),
            "webinars": lecturer_service.get_lecturer_webinars(),
            "archived_webinars": lecturer_service.get_lecturer_webinars_archived(),
        },
    )
