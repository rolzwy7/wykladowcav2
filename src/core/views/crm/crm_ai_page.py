"""CRM AI"""

# flake8: noqa=E501

from django.conf import settings
from django.template.response import TemplateResponse

from core.models import Lecturer, WebinarAggregate


def crm_ai_page(request):
    """crm_ai_page"""
    template_name = "core/pages/crm/CrmAiPage.html"
    return TemplateResponse(
        request,
        template_name,
        {},
    )


def crm_ai_konsensus(request):
    """crm_ai_konsensus"""
    template_name = "core/pages/crm/Konsensus.txt"

    active_lecturers = Lecturer.manager.filter(
        id__in=list(
            set(
                [
                    _.lecturer.id
                    for _ in WebinarAggregate.manager.filter(has_active_webinars=True)
                ]
            )
        )
    )

    aggregates = WebinarAggregate.manager.get_active_aggregates()

    return TemplateResponse(
        request,
        template_name,
        {
            "active_lecturers": active_lecturers,
            "aggregates": aggregates,
            "BASE_URL": settings.BASE_URL,
        },
        content_type="text/plain; charset=utf-8",
    )
