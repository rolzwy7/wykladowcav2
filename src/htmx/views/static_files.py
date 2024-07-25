"""Static files"""

# pylint: disable=unused-variable
# pylint: disable=broad-exception-caught
# flake8: noqa=F841

from pathlib import Path

from django.conf import settings
from django.template.response import TemplateResponse
from django.views.decorators.cache import cache_page

BASE_DIR = settings.BASE_DIR
ASSETS_DIR: Path = BASE_DIR.parent / "public" / "static"


@cache_page(60)
def disc_space(request):
    """Celery workers"""
    template_name = "htmx/static_files/disc_space.html"

    filepath = ASSETS_DIR / "disc_space.txt"

    if filepath.exists() and filepath.is_file():
        try:
            date, taken, no_recordings = filepath.open("r").readlines()
        except Exception as e:
            date, taken, no_recordings = "error", "error", "error"
    else:
        date, taken, no_recordings = "no_file", "no_file", "no_file"

    date = date.strip()
    taken = taken.strip()
    no_recordings = no_recordings.strip()

    try:
        taken_num = float(taken)
        progress_bar_width = int(100 * taken_num / 200.0)
        if progress_bar_width > 90:
            progress_bar_color = "danger"
        elif progress_bar_width > 70:
            progress_bar_color = "warning"
        else:
            progress_bar_color = "success"

    except Exception as e:
        progress_bar_color = "secondary"
        progress_bar_width = "50"

    return TemplateResponse(
        request,
        template_name,
        {
            "date": date.strip(),
            "taken": taken.strip(),
            "no_recordings": no_recordings.strip(),
            "progress_bar_color": progress_bar_color,
            "progress_bar_width": progress_bar_width,
        },
    )
