"""
Consts context processor
"""

# flake8: noqa=E501

from django.core.cache import cache

from core.models import Webinar


def cached(request):
    """Settings context processor"""

    cached_dict = {}

    # Count active webinars
    cache_key = "CACHED_ACTIVE_WEBINARS_COUNT"
    cache_seconds = 15 * 60  # 15 minutes
    if cache.get(cache_key):
        cached_dict[cache_key] = cache.get(cache_key)
    else:
        cached_dict[cache_key] = Webinar.manager.get_active_webinars().count()
        cache.set(cache_key, cached_dict[cache_key], timeout=cache_seconds)

    return cached_dict
