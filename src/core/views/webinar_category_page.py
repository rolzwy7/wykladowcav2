from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar, WebinarCategory


def webinar_all_categories_page(request):
    """Webinar all categories page"""

    template_name = "geeks/pages/category/WebinarAllCategoriesPage.html"
    category_name = "Wszystkie szkolenia"
    # short_description = ""
    # webinars = Webinar.manager.homepage_webinars()
    subcategories = WebinarCategory.manager.sidebar_categories()

    return TemplateResponse(
        request,
        template_name,
        {
            "slug": "wszystkie",
            "category_name": category_name,
            # "webinars": webinars,
            # "short_description": short_description,
            "subcategories": subcategories,
        },
    )


def webinar_category_page(request, slug: str):
    """Webinar category page"""

    template_name = "geeks/pages/category/WebinarCategoryPage.html"
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


def webinar_category_who_are_we_page(request, slug: str):
    """Webinar category page"""

    template_name = "geeks/pages/category/WebinarCategoryWhoAreWePage.html"
    category = get_object_or_404(WebinarCategory, slug=slug)

    return TemplateResponse(
        request,
        template_name,
        {"slug": slug, "category": category, "category_name": category.name},
    )


def webinar_category_lecturer_page(request, slug: str):
    """Webinar category page"""

    template_name = "geeks/pages/category/WebinarCategoryLecturerPage.html"
    category = get_object_or_404(WebinarCategory, slug=slug)

    return TemplateResponse(
        request,
        template_name,
        {"slug": slug, "category": category, "category_name": category.name},
    )


def webinar_category_opinions_page(request, slug: str):
    """Webinar category page"""

    template_name = "geeks/pages/category/WebinarCategoryOpinionsPage.html"
    category = get_object_or_404(WebinarCategory, slug=slug)

    return TemplateResponse(
        request,
        template_name,
        {"slug": slug, "category": category, "category_name": category.name},
    )
