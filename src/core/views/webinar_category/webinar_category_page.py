"""
Category pages
"""

# flake8: noqa:E501
# pylint: disable=line-too-long

from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.models import CategoryTrustedUs, Webinar, WebinarAggregate, WebinarCategory


def webinar_category_page(request, slug: str):
    """Webinar category page"""

    template_name = "geeks/pages/category/WebinarCategoryPage.html"

    category = get_object_or_404(WebinarCategory, slug=slug)

    if category.parent:
        return redirect(
            reverse("core:webinar_category_page", kwargs={"slug": category.parent.slug})
        )

    # trusted_us = CategoryTrustedUs.manager.get_visible().filter(category=category)
    menu_categories = WebinarCategory.manager.get_subcategories(category)
    # archived_webinars = (
    #     Webinar.manager.get_archived_webinars_for_category_slugs(
    #         [slug, *[_.slug for _ in menu_categories]]
    #     )
    # )
    # webinars = Webinar.manager.get_active_webinars_for_category_slugs(
    #     [slug, *[_.slug for _ in menu_categories]]
    # )
    aggregates = WebinarAggregate.manager.get_active_aggregates_for_category_slugs(
        [slug, *[_.slug for _ in menu_categories]]
    )

    return TemplateResponse(
        request,
        template_name,
        {
            "category": category,
            "slug": slug,
            # "webinars": webinars,
            "aggregates": aggregates,
            # "archived_webinars": archived_webinars,
            # "webinars_count": webinars.count(),
            "menu_categories": menu_categories,
            # "trusted_us": trusted_us,
        },
    )
