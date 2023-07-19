from pathlib import Path

from django.conf import settings
from django.http import HttpRequest, HttpResponse

BASE_DIR = settings.BASE_DIR
BASE_URL = settings.BASE_URL


def robots_page(request: HttpRequest):
    """Robots page"""
    robots_path: Path = BASE_DIR.parent / "core" / "assets" / "robots.txt"
    content = robots_path.open("rb").read()

    sitemap_url = f"{BASE_URL}/sitemap.xml"
    content = content.replace(b"[SITEMAP_URL]", sitemap_url.encode())

    return HttpResponse(content, content_type="text/plain")
