"""Static files"""

# pylint: disable=unused-variable
# pylint: disable=broad-exception-caught
# flake8: noqa=F841

from pathlib import Path

from django.conf import settings
from django.template.response import TemplateResponse
from django.views.decorators.cache import cache_page

from core.services import StaticFilesIndicatorsService

BASE_DIR = settings.BASE_DIR
ASSETS_DIR: Path = BASE_DIR.parent / "public" / "static"


@cache_page(60)
def disc_space(request):
    """Celery workers"""
    template_name = "htmx/static_files/disc_space.html"

    service = StaticFilesIndicatorsService()

    return TemplateResponse(request, template_name, service.get_disc_space_context())
