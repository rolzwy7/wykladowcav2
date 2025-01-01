"""
Category pages
"""

# flake8: noqa:E501
# pylint: disable=line-too-long

from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import CategoryTrustedUs, Webinar, WebinarCategory


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
        # archived_webinars = Webinar.manager.get_archived_webinars()
        parent = None
        trusted_us = []
        page_title = "Wszystkie szkolenia"

    elif slug == "darmowe-webinary":
        category_name = "Bezpłatne webinary"
        menu_categories = WebinarCategory.manager.get_main_categories()
        webinars = Webinar.manager.get_active_conferences()
        # archived_webinars = None
        parent = None
        trusted_us = []
        page_title = "Bezpłatne webinary"
    else:
        category = get_object_or_404(WebinarCategory, slug=slug)
        category_name = category.name
        parent = category.parent
        trusted_us = CategoryTrustedUs.manager.get_visible().filter(category=category)
        if parent:
            page_title = f"{parent.name} > {category.name}"
            menu_categories = WebinarCategory.manager.get_subcategories(parent)
            # archived_webinars = (
            #     Webinar.manager.get_archived_webinars_for_category_slugs([slug])
            # )
            webinars = Webinar.manager.get_active_webinars_for_category_slugs([slug])
        else:
            page_title = category.name
            menu_categories = WebinarCategory.manager.get_subcategories(category)
            # archived_webinars = (
            #     Webinar.manager.get_archived_webinars_for_category_slugs(
            #         [slug, *[_.slug for _ in menu_categories]]
            #     )
            # )
            webinars = Webinar.manager.get_active_webinars_for_category_slugs(
                [slug, *[_.slug for _ in menu_categories]]
            )

    return TemplateResponse(
        request,
        template_name,
        {
            "slug": slug,
            "page_title": page_title,
            "parent": parent,
            "webinars": webinars,
            # "archived_webinars": archived_webinars,
            "webinars_count": webinars.count(),
            "short_description": short_description,
            "menu_categories": menu_categories,
            "category_name": category_name,
            "trusted_us": trusted_us,
        },
    )
