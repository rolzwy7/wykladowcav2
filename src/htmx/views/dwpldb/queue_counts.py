"""Health indicator"""

# flake8: noqa=E501

from django.core.cache import cache
from django.http import HttpResponse

from core.libs.mongo.db import get_dwpldbv3_connection


def regon_queue_count(request):
    """regon_queue_count"""

    # Count active webinars
    cache_key = "CACHED_REGON_QUEUE_COUNT"
    cache_seconds = 15 * 60  # 15 minutes

    if cache.get(cache_key):
        count = cache.get(cache_key)
    else:
        client, db = get_dwpldbv3_connection()
        count = db["regon_queue"].count_documents({})
        client.close()
        cache.set(cache_key, count, timeout=cache_seconds)

    return HttpResponse(f"{count:,}")


def email_verify_queue_count(request):
    """email_verify_queue_count"""

    # Count active webinars
    cache_key = "CACHED_EMAIL_VERIFY_QUEUE_COUNT"
    cache_seconds = 15 * 60  # 15 minutes

    if cache.get(cache_key):
        count = cache.get(cache_key)
    else:
        client, db = get_dwpldbv3_connection()
        count = db["email_verify_queue"].count_documents({})
        client.close()
        cache.set(cache_key, count, timeout=cache_seconds)

    return HttpResponse(f"{count:,}")


def scraper_queue_static_count(request):
    """scraper_queue_static_count"""

    # Count active webinars
    cache_key = "CACHED_SCRAPER_QUEUE_STATIC_COUNT"
    cache_seconds = 15 * 60  # 15 minutes

    if cache.get(cache_key):
        count = cache.get(cache_key)
    else:
        client, db = get_dwpldbv3_connection()
        count = db["scraper_queue_static"].count_documents({})
        client.close()
        cache.set(cache_key, count, timeout=cache_seconds)

    return HttpResponse(f"{count:,}")
