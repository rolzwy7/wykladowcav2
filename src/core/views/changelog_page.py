from pathlib import Path

from django.conf import settings
from django.http import HttpRequest, HttpResponse

BASE_DIR = settings.BASE_DIR


def changelog_page(request: HttpRequest):
    """Changelog page"""
    path: Path = BASE_DIR.parent / "core" / "assets" / "changelog.txt"
    content = path.open("rb").read()

    return HttpResponse(content, content_type="text/plain; charset=utf-8")
