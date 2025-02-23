"""Health indicator"""

# flake8: noqa=E501

from django.core.cache import cache
from django.http import HttpResponse
from django.template.response import TemplateResponse

from core.libs.mongo.db import get_dwpldbv3_connection


def scraper_procedure_progress(request, collection_fragment: str):
    """scraper_procedure_progress"""

    template_path = "htmx/scraper_procedure_progress.html"
    cache_key = f"CACHED_SCRAPER_PROCEDURE_PROGRESS_{collection_fragment}"
    cache_seconds = 60 * 60  # 60 minutes

    if cache.get(cache_key):
        context = cache.get(cache_key)
    else:
        client, db = get_dwpldbv3_connection()

        done_queue = db[f"scraper_{collection_fragment}_queue"].count_documents(
            {"bucket": 999}
        )
        estimated_count = db[
            f"scraper_{collection_fragment}_queue"
        ].estimated_document_count()

        context = {
            "collection_fragment": collection_fragment,
            "done_queue": f"{done_queue:,}",
            "estimated_count": f"{estimated_count:,}",
            "percent_done": f"{done_queue / estimated_count:.2%}",
        }

        client.close()
        cache.set(cache_key, context, timeout=cache_seconds)

    return TemplateResponse(request, template_path, context)
