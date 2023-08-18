from django.urls import reverse

from core.models import WebinarCategory


def header(request):
    """Header context processor"""

    sidebar_categories_qs = WebinarCategory.manager.sidebar_categories()

    header_categories = []
    for category in sidebar_categories_qs:
        if not category.parent:
            header_categories.append(
                (
                    category.name,
                    reverse(
                        "core:webinar_category_page",
                        kwargs={"slug": category.slug},
                    ),
                    category.short_description,
                    category.icon_html,
                )
            )

    return {
        "HEADER_CATEGORIES": header_categories,
    }
