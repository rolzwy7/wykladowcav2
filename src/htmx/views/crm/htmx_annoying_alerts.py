"""htmx_annoying_alerts"""

from django.db.models import Q
from django.http import HttpRequest
from django.template.response import TemplateResponse

from core.models import Lecturer

# flake8: noqa


def htmx_annoying_alerts(request: HttpRequest):
    """CRM check nip"""
    template_path = "htmx/htmx_annoying_alerts.html"

    chomato_activated = False

    # Wykladowcy ktorzy nie maja uzupelnionych fake liczby szkolen i uczestnikow
    lecturers_no_fake = Lecturer.manager.filter(
        Q(fake_stat_participants=0) | Q(fake_stat_webinars=0)
    )
    if lecturers_no_fake.exists():
        chomato_activated = True

    return TemplateResponse(
        request,
        template_path,
        {
            "chomato_activated": chomato_activated,
            "lecturers_no_fake": lecturers_no_fake,
        },
    )
