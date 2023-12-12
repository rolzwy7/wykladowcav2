"""
Consts context processor
"""

# flake8: noqa=E501

from django.core.cache import cache

from core.models import Webinar, WebinarCategory


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

    return cached_dict
