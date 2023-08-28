from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar, WebinarCategory


def webinar_category_page(request, slug: str):
    """Webinar category page"""
    template_name = "geeks/pages/category/WebinarCategoryPage.html"

    if slug == "wszystkie":
        category_name = "Wszystkie szkolenia"
        short_description = ""
        webinars = Webinar.manager.homepage_webinars()
        subcategories = WebinarCategory.manager.sidebar_categories()
    else:
        category = get_object_or_404(WebinarCategory, slug=slug)
        category_name = category.name
        short_description = category.short_description
        webinars = Webinar.manager.webinars_for_category(slug)
        subcategories = WebinarCategory.manager.get_subcategories(category)

    return TemplateResponse(
        request,
        template_name,
        {
            "slug": slug,
            "category_name": category_name,
            "webinars": webinars,
            "short_description": short_description,
            "subcategories": subcategories,
        },
    )
