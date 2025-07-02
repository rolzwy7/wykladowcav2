"""
Webmap page
"""

# flake8: noqa=E501

from django.template.response import TemplateResponse

from core.models import Lecturer, WebinarAggregate, WebinarCategory


def webmap_page(request):
    """Webmap controller"""
    template_path = "geeks/pages/WebmapPage.html"

    active_aggregates = WebinarAggregate.manager.get_active_aggregates()

    categories = WebinarCategory.manager.get_visible_categories()
    lecturers = Lecturer.manager.get_lecturers_visible_on_page()

    return TemplateResponse(
        request,
        template_path,
        {
            "active_aggregates": active_aggregates,
            "categories": categories,
            "lecturers": lecturers,
        },
    )
