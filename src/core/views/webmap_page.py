"""
Webmap page
"""

# flake8: noqa=E501

from django.template.response import TemplateResponse

from core.models import Lecturer, Webinar, WebinarCategory


def webmap_page(request):
    """Webmap controller"""
    template_path = "geeks/pages/WebmapPage.html"

    archived_webinars = Webinar.manager.get_archived_webinars()
    active_webinars = Webinar.manager.get_active_webinars()

    categories = WebinarCategory.manager.get_visible_categories()
    lecturers = Lecturer.manager.get_lecturers_visible_on_page()

    return TemplateResponse(
        request,
        template_path,
        {
            "archived_webinars": archived_webinars,
            "active_webinars": active_webinars,
            "categories": categories,
            "lecturers": lecturers,
        },
    )
