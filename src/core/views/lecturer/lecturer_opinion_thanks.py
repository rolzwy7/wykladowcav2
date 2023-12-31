from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Lecturer


def lecturer_opinion_thanks(request, slug: str):
    """lecturer_opinion_thanks"""
    template_name = "geeks/pages/lecturer/LecturerOpinionThanksPage.html"
    lecturer = get_object_or_404(Lecturer, slug=slug)

    return TemplateResponse(
        request,
        template_name,
        {
            "lecturer": lecturer,
        },
    )
