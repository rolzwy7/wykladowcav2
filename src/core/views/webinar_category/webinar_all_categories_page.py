"""
Category pages
"""

# flake8: noqa:E501
# pylint: disable=line-too-long

from django.template.response import TemplateResponse


def webinar_all_categories_page(request):
    """Webinar all categories page"""

    template_name = "geeks/pages/category/WebinarAllCategoriesPage.html"

    return TemplateResponse(
        request,
        template_name,
        {},
    )
