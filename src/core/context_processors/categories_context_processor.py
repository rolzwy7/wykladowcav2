from django.core.cache import cache
from django.urls import reverse

from core.models import Webinar, WebinarCategory


def categories(request):
    """Categories context processor"""

    # Process the context only on chosen paths
    if not request.path.startswith("/szkolenia/"):
        return []

    # If sidebar categories exist in cache return them
    cached_data = cache.get("CORE:SIDEBAR_CATEGORIES")
    if cached_data is not None:
        return {"SIDEBAR_CATEGORIES": cached_data}

    # Get sidebar categories
    sidebar_categories_qs = WebinarCategory.manager.sidebar_categories()

    # Build sidebar categories
    sidebar_categories = [
        (
            category.order,
            Webinar.manager.homepage_webinars()
            .filter(categories__in=[category])
            .count(),
            category.name,
            reverse(
                "core:webinar_category_page",
                kwargs={"slug": category.slug},
            ),
        )
        for category in sidebar_categories_qs
    ]

    # Sort by order
    sidebar_categories = sorted(sidebar_categories, key=lambda x: x[0])

    # Cache for 4 hours
    modified_copy = sidebar_categories.copy()
    cache.set("CORE:SIDEBAR_CATEGORIES", modified_copy, timeout=60 * 60 * 4)

    return {
        "SIDEBAR_CATEGORIES": sidebar_categories,
    }
