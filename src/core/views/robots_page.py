from pathlib import Path

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.views.decorators.cache import cache_page

BASE_DIR = settings.BASE_DIR
BASE_URL = settings.BASE_URL


@cache_page(60 * 60)
def robots_page(request: HttpRequest):
    """Robots page"""
    robots_path: Path = BASE_DIR.parent / "core" / "assets" / "robots.txt"
    content = robots_path.open("rb").read()

    sitemap_url = f"{BASE_URL}/sitemap.xml"

    # Add sitemap url
    content += f"Sitemap: {sitemap_url}\n".encode()

    # Prevent indexing in staging environment
    if settings.APP_ENV in ["develop", "staging"]:
        content += b"X-Robots-Tag: noindex\n"

    return HttpResponse(content, content_type="text/plain")
