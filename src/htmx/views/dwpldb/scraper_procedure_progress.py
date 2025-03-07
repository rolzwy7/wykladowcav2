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
    cache_seconds = 20 * 60  # 20 minutes

    if cache.get(cache_key):
        context = cache.get(cache_key)
    else:
        client, db = get_dwpldbv3_connection()

        done_queue = db[f"scraper_{collection_fragment}_queue"].count_documents(
            {"bucket": 999}
        )
        estimated_queue_count = db[
            f"scraper_{collection_fragment}_queue"
        ].estimated_document_count()

        estimated_init_count = db[
            f"scraper_{collection_fragment}_init"
        ].estimated_document_count()

        estimated_html_count = db[
            f"scraper_{collection_fragment}_html"
        ].estimated_document_count()

        # Get storage size
        stats = db.command("collStats", f"scraper_{collection_fragment}_html")
        storage_size = stats.get("storageSize", 0)  # Storage size in bytes
        if storage_size != 0:
            html_size_gb = storage_size / (1024**3)
        else:
            html_size_gb = -1

        # Analyzers
        total_analyzed = 0
        analyzers = []
        for doc in db["vars_map"].find({"kod_procedury": collection_fragment}):
            total_analyzed += doc["analyze_counter"]
            analyzers.append(
                (
                    doc["hostname"],
                    doc["status"],
                    doc["analyze_counter"],
                    doc["analyze_dir"],
                    doc["datetime"],
                )
            )

        if done_queue == 0:
            total_analyzed_percent = 0
        else:
            total_analyzed_percent = total_analyzed / done_queue

        context = {
            "collection_fragment": collection_fragment,
            "done_queue": f"{done_queue:,}",
            "estimated_queue_count": f"{estimated_queue_count:,}",
            "estimated_init_count": f"{estimated_init_count:,}",
            "estimated_html_count": f"{estimated_html_count:,}",
            "percent_done": f"{done_queue / estimated_queue_count:.2%}",
            "html_size_gb": f"{html_size_gb:.1f}",
            "analyzers": analyzers,
            "total_analyzed": f"{total_analyzed:,}",
            "total_analyzed_percent": f"{total_analyzed_percent:.2%}",
        }

        client.close()
        cache.set(cache_key, context, timeout=cache_seconds)

    return TemplateResponse(request, template_path, context)
