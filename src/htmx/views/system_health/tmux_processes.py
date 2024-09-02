"""Health indicator"""

# pylint: disable=unused-variable
# pylint: disable=broad-exception-caught
# flake8: noqa=F841

from pathlib import Path

from django.conf import settings
from django.template.response import TemplateResponse

from core.services import StaticFilesIndicatorsService

BASE_DIR = settings.BASE_DIR
ASSETS_DIR: Path = BASE_DIR.parent / "public" / "static"


def tmux_processes(request):
    """Tmux processes"""
    template_name = "htmx/system_health/tmux_processes.html"

    service = StaticFilesIndicatorsService()

    return TemplateResponse(
        request, template_name, service.get_tmux_processes_context()
    )
