# flake8: noqa=E501

from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Lecturer, Webinar


def lecturer_mailing_template_page(request: HttpRequest, slug: str):
    """Webinar email template page"""
    template_name = "mailing_templates/LecturerMailingTemplate.html"
    lecturer = get_object_or_404(Lecturer, slug=slug)

    lecturer_id: int = lecturer.id  # type: ignore
    webinars = Webinar.manager.get_active_webinars_for_lecturer(lecturer_id=lecturer_id)

    ctx = {}

    def _split_pairs(seq):
        ret = []
        for i in range(0, len(seq) + 1, 2):
            ret.append(seq[i : i + 2])
        return ret

    # Create keys for durations
    for _ in webinars:
        ctx[_.get_duration_display()] = []  # type: ignore

    for _ in webinars:
        ctx[_.get_duration_display()].append(_)  # type: ignore

    for key, value in ctx.items():
        ctx[key] = _split_pairs(value)

    return TemplateResponse(
        request,
        template_name,
        {
            "BASE_URL": settings.BASE_URL,
            "lecturer": lecturer,
            "webinars_map": ctx,
            "background_color": "#f1f4fa",
            "max_width": "640px",
            "td_classes": (
                "border-collapse:collapse;"
                "padding-left:20px;"
                "padding-right:20px;"
                "font-size: 16px;"
            ),
        },
    )
