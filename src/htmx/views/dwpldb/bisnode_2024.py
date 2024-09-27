"""Health indicator"""

# flake8: noqa=E501

from django.core.cache import cache
from django.http import HttpResponse

from core.libs.mongo.db import get_dwpldbv3_connection


def bisnode_2024_download_progress(request):
    """bisnode_2024_download_progress"""

    # Count active webinars
    cache_key = "CACHED_BISNODE_2024_DOWNLOAD_PROGRESS"
    cache_seconds = 5 * 60  # 5 minute

    if cache.get(cache_key):
        percent = cache.get(cache_key)
    else:
        client, db = get_dwpldbv3_connection()
        document = db["download_bisnode_2024_progress"].find_one(
            {"status": {"$eq": "PROGRESS"}}
        )
        if document:
            doc_id: str = document["_id"]
            doc_id_int = int(doc_id.replace("-", ""))
            percent = f"{(doc_id_int/100_000):.2%}"
        else:
            percent = "error %"
        client.close()
        cache.set(cache_key, percent, timeout=cache_seconds)

    return HttpResponse(percent)
