from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models.lecturer_model import Lecturer


def lecturer_stats_page(request, pk: int):
    """Lecturer stats page"""
    template_name = "core/pages/crm/lecturer/LecturerStatsPage.html"
    lecturer = get_object_or_404(Lecturer, pk=pk)
    return TemplateResponse(request, template_name, {"lecturer": lecturer})
