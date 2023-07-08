from django.urls import reverse

from core.models import WebinarCategory

HEADER = "HEADER"
ITEM = "ITEM"


def categories(request):
    """Categories context processor"""

    # TODO: Caching
    # TODO: Active category
    # TODO: Document this

    sidebar_categories_qs = WebinarCategory.manager.sidebar_categories()

    sidebar_categories = []
    for category in sidebar_categories_qs:
        if category.parent:
            sidebar_categories.append(
                (
                    ITEM,
                    category.order + 1,
                    reverse(
                        "core:webinar_category_page",
                        kwargs={"slug": category.slug},
                    ),
                    category.name,
                )
            )
        else:
            sidebar_categories.append(
                (
                    HEADER,
                    category.order,
                    reverse(
                        "core:webinar_category_page",
                        kwargs={"slug": category.slug},
                    ),
                    category.name,
                )
            )
            sidebar_categories.append(
                (
                    ITEM,
                    category.order + 1,
                    "/"
                    if category.is_homepage_category
                    else reverse(
                        "core:webinar_category_page",
                        kwargs={"slug": category.slug},
                    ),
                    "Wszystkie",
                )
            )

    sidebar_categories = sorted(sidebar_categories, key=lambda x: x[1])

    return {"SIDEBAR_CATEGORIES": sidebar_categories}
