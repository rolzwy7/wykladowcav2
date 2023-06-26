from django.urls import reverse

from core.models import WebinarCategory

HEADER = "HEADER"
ITEM = "ITEM"


def categories(request):
    """Adds categories into global context"""
    # TODO: Caching
    # TODO: Active category
    # TODO: Document this

    sidebar_categories_qs = WebinarCategory.manager.sidebar_categories()

    sidebar_categories = []
    for category in sidebar_categories_qs:
        # TODO: in english please
        # If parent add after it "all" url
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
                    reverse(
                        "core:webinar_category_page",
                        kwargs={"slug": category.slug},
                    ),
                    "Wszystkie",
                )
            )

    # TODO: Sorting

    sidebar_categories = sorted(sidebar_categories, key=lambda x: x[1])

    return {"SIDEBAR_CATEGORIES": sidebar_categories}
