from django.urls import reverse

from core.models import Webinar, WebinarCategory

HEADER = "HEADER"
ITEM = "ITEM"


def categories(request):
    """Categories context processor"""

    sidebar_categories_qs = WebinarCategory.manager.sidebar_categories()

    sidebar_categories = []
    for category in sidebar_categories_qs:
        category_count = (
            Webinar.manager.init_or_confirmed()
            .filter(categories__in=[category])
            .count()
        )

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
                    category_count,
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
                    category_count,
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
                    None,
                )
            )

    sidebar_categories = sorted(sidebar_categories, key=lambda x: x[1])

    return {"SIDEBAR_CATEGORIES": sidebar_categories}
