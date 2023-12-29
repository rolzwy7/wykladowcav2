"""
Category pages
"""

# flake8: noqa:E501
# pylint: disable=line-too-long

from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import LecturerOpinion, WebinarCategory
from core.services import CategoryService, OpinionsService


def webinar_category_opinions_page(request, slug: str):
    """Webinar category page"""

    template_name = "geeks/pages/category/WebinarCategoryOpinionsPage.html"

    page_number = request.GET.get("strona")

    if slug == "wszystkie-szkolenia":
        category_name = "Wszystkie szkolenia"
        category_opinions = LecturerOpinion.manager.get_all_visible_opinions()
    else:
        category = get_object_or_404(WebinarCategory, slug=slug)
        category_service = CategoryService(category)
        category_opinions = category_service.get_opinions_for_category()
        category_name = category.name

    opinions_service = OpinionsService(category_opinions)

    return TemplateResponse(
        request,
        template_name,
        {
            "slug": slug,
            "category_name": category_name,
            "opinions_page": opinions_service.get_opinions_page(
                page_number, per_page=7
            ),
            "opinions_count": category_opinions.count(),
            "opinions_average": opinions_service.get_opinions_average(),
            "opinions_breakdown": opinions_service.get_opinions_breakdown(),
        },
    )
