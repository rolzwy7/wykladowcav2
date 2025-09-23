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

    category = get_object_or_404(WebinarCategory, slug=slug)

    # TODO: Przekieruj do rodzica
    # if category.parent:
    #     return redirect(
    #         reverse("core:webinar_category_page", kwargs={"slug": category.parent.slug})
    #     )

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

    cat_column_a = []
    cat_column_b = []
    cat_column_c = []
    for idx, menu_category in enumerate(menu_categories):
        if idx % 3 == 0:
            cat_column_a.append(menu_category)
        if idx % 3 == 1:
            cat_column_b.append(menu_category)
        if idx % 3 == 2:
            cat_column_c.append(menu_category)

    return TemplateResponse(
        request,
        "geeks/pages/category/WebinarCategoryPage.html",
        {
            "category": category,
            "slug": slug,
            # "webinars": webinars,
            "aggregates": aggregates,
            # "archived_webinars": archived_webinars,
            # "webinars_count": webinars.count(),
            "menu_categories": menu_categories,
            # "trusted_us": trusted_us,
            "cat_column_a": cat_column_a,
            "cat_column_b": cat_column_b,
            "cat_column_c": cat_column_c,
        },
    )
