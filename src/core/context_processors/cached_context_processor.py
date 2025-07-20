"""
Consts context processor
"""

# flake8: noqa=E501

from django.core.cache import cache
from django.template.defaultfilters import date as _date
from django.urls import reverse
from django.utils.timezone import get_default_timezone, now

from core.models import (
    ServiceOfferApplication,
    Webinar,
    WebinarAggregate,
    WebinarCategory,
)


def cached(request):
    """Settings context processor"""

    cached_dict = {}

    # Count active webinars
    cache_key = "CACHED_ACTIVE_WEBINARS_COUNT"
    cache_seconds = 5 * 60  # 5 minutes
    if cache.get(cache_key):
        cached_dict[cache_key] = cache.get(cache_key)
    else:
        cached_dict[cache_key] = Webinar.manager.get_active_webinars().count()
        cache.set(cache_key, cached_dict[cache_key], timeout=cache_seconds)

    # Get main categories wiyh counts
    cache_key = "CACHED_MAIN_CATEGORIES"
    cache_seconds = 60 * 60  # 1 hour
    if cache.get(cache_key):
        cached_dict[cache_key] = cache.get(cache_key)
    else:
        main_categories = WebinarCategory.manager.get_main_categories()
        seq = []
        for category in main_categories:
            seq.append(
                (
                    category,
                    Webinar.manager.get_active_webinars_for_category_slugs(
                        [category.slug]
                    ).count(),
                    WebinarCategory.manager.get_subcategories(category),
                )
            )
        cached_dict[cache_key] = seq
        cache.set(cache_key, cached_dict[cache_key], timeout=cache_seconds)

    # Get service applications sent today
    cache_key = "CACHED_SERVICE_APPLICATIONS_SENT_TODAY"
    cache_seconds = 60 * 60  # 1 hour
    if cache.get(cache_key):
        cached_dict[cache_key] = cache.get(cache_key)
    else:

        cached_dict[cache_key] = ServiceOfferApplication.manager.filter(
            created_at__date=now().date()
        ).count()
        cache.set(cache_key, cached_dict[cache_key], timeout=cache_seconds)

    # Get service applications sent today
    cache_key = "CACHED_MEGAMENU"
    cache_seconds = 60 * 60  # 1 hour
    if cache.get(cache_key):
        cached_dict[cache_key] = cache.get(cache_key)
    else:
        menu_data = {}

        def get_megamenu_result(aggregate: WebinarAggregate):
            """get_megamenu_result"""
            tz = get_default_timezone()
            dates = []

            for webinar in aggregate.webinars.all():
                if webinar.is_active:
                    dates.append(
                        f"{_date(webinar.date.astimezone(tz), 'j E Y')} godz. {_date(webinar.date.astimezone(tz), 'H:i')}"
                    )

            return {
                "title": aggregate.title,
                "url": reverse(
                    "core:webinar_aggregate_page", kwargs={"slug": aggregate.slug}
                ),
                "avatar": f"/media/uploads/lecturers/{aggregate.lecturer.slug}_80x80.webp" if not aggregate.is_anonymized else "/static/default/default-lecturer-avatar-80x80.webp",  # type: ignore
                "lecturer_fullname": aggregate.lecturer.fullname if not aggregate.is_anonymized else "",  # type: ignore
                "dates": dates,
                "price": f"{aggregate.minimal_price}",
            }

        for main_cat in WebinarCategory.manager.get_main_categories():
            subcategories = []

            for _ in WebinarCategory.manager.get_subcategories(main_cat):
                any_aggregates = (
                    WebinarAggregate.manager.get_active_aggregates_for_category_slugs(
                        slugs=[_.slug]
                    )
                )
                if any_aggregates:
                    subcategories.append(_.name)

            menu_data[f"{main_cat.name_homepage}"] = {
                "subcategories": subcategories,
                "results": {
                    "Wszystko": [
                        get_megamenu_result(agg)
                        for agg in WebinarAggregate.manager.get_active_aggregates_for_category_slugs(
                            slugs=[main_cat.slug]
                        )
                    ],
                    **{
                        f"{subcat.name}": [
                            get_megamenu_result(agg)
                            for agg in WebinarAggregate.manager.get_active_aggregates_for_category_slugs(
                                slugs=[subcat.slug]
                            )
                        ]
                        for subcat in WebinarCategory.manager.get_subcategories(
                            main_cat
                        )
                    },
                },
            }

        cached_dict[cache_key] = menu_data
        cache.set(cache_key, cached_dict[cache_key], timeout=cache_seconds)

    return cached_dict
