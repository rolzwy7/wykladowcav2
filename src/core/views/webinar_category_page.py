"""
Category pages
"""

# flake8: noqa:E501
# pylint: disable=line-too-long

from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import CategoryTrustedUs, LecturerOpinion, Webinar, WebinarCategory
from core.services import CategoryService, OpinionsService


def webinar_all_categories_page(request):
    """Webinar all categories page"""

    template_name = "geeks/pages/category/WebinarAllCategoriesPage.html"

    return TemplateResponse(
        request,
        template_name,
        {},
    )


def webinar_category_page(request, slug: str):
    """Webinar category page"""

    template_name = "geeks/pages/category/WebinarCategoryPage.html"

    page_title: str = ""
    category_name: str = ""
    short_description: str = ""

    if slug == "wszystkie-szkolenia":
        category_name = "Wszystkie szkolenia"
        menu_categories = WebinarCategory.manager.get_main_categories()
        webinars = Webinar.manager.get_active_webinars()
        parent = None
        trusted_us = []
    else:
        category = get_object_or_404(WebinarCategory, slug=slug)
        category_name = category.name
        parent = category.parent
        trusted_us = CategoryTrustedUs.manager.get_visible().filter(category=category)
        if parent:
            page_title = f"{parent.name} > {category.name}"
            menu_categories = WebinarCategory.manager.get_subcategories(parent)
        else:
            page_title = category.name
            menu_categories = WebinarCategory.manager.get_subcategories(category)

        webinars = Webinar.manager.get_active_webinars_for_category_slugs(
            [slug, *[_.slug for _ in menu_categories]]  # TODO: delete slug ?
        )

    return TemplateResponse(
        request,
        template_name,
        {
            "slug": slug,
            "page_title": page_title,
            "parent": parent,
            "webinars": webinars,
            "webinars_count": webinars.count(),
            "short_description": short_description,
            "menu_categories": menu_categories,
            "category_name": category_name,
            "trusted_us": trusted_us,
        },
    )


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
