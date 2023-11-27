# flake8: noqa:E501
# pylint: disable=line-too-long

from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar, WebinarCategory
from core.services import CategoryService, OpinionsService


def webinar_all_categories_page(request):
    """Webinar all categories page"""

    template_name = "geeks/pages/category/WebinarAllCategoriesPage.html"
    category_name = "Wszystkie kategorie szkoleń"
    # short_description = ""
    # webinars = Webinar.manager.homepage_webinars()

    subcategories = CategoryService.get_all_categories_with_counts()

    return TemplateResponse(
        request,
        template_name,
        {
            "slug": "wszystkie-kategorie",
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

    subcategories = WebinarCategory.manager.get_subcategories(category)

    slugs = [slug, *[subcategory.slug for subcategory in subcategories]]
    webinars = Webinar.manager.get_active_webinars_for_category_slugs(slugs)

    return TemplateResponse(
        request,
        template_name,
        {
            "slug": slug,
            "category": category,
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


def webinar_category_lecturers_page(request, slug: str):
    """Page with lecturers for given category"""

    template_name = "geeks/pages/category/WebinarCategoryLecturerPage.html"
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


def webinar_category_opinions_page(request, slug: str):
    """Webinar category page"""

    template_name = "geeks/pages/category/WebinarCategoryOpinionsPage.html"
    category = get_object_or_404(WebinarCategory, slug=slug)
    category_service = CategoryService(category)
    category_opinions = category_service.get_opinions_for_category()
    opinions_service = OpinionsService(category_opinions)
    page_number = request.GET.get("strona")

    return TemplateResponse(
        request,
        template_name,
        {
            "slug": slug,
            "category": category,
            "category_name": category.name,
            "opinions_page": opinions_service.get_opinions_page(
                page_number, per_page=15
            ),
            "opinions_average": opinions_service.get_opinions_average(),
            "opinions_breakdown": opinions_service.get_opinions_breakdown(),
        },
    )
