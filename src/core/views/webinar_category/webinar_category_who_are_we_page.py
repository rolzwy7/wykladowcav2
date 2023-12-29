"""
Category pages
"""

# flake8: noqa:E501
# pylint: disable=line-too-long

from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import WebinarCategory
from core.services import CategoryService


def webinar_category_who_are_we_page(request, slug: str):
    """Webinar category page"""

    template_name = "geeks/pages/category/WebinarCategoryWhoAreWePage.html"
    category = get_object_or_404(WebinarCategory, slug=slug)
    category_service = CategoryService(category)

    return TemplateResponse(
        request,
        template_name,
        {
            "slug": slug,
            "category": category,
            "category_name": category.name,
            "category_lecturers": category_service.get_lecturers_for_category(),
        },
    )
