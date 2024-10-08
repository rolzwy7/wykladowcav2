"""HTMX URLs"""

# flake8: noqa=E501

from django.urls import path

from .celery_workers import celery_workers
from .health_indicator import health_indicator
from .tmux_processes import tmux_processes

app_name = "system-health"  # pylint: disable=invalid-name

urlpatterns = [
    path(
        "indicator/",
        health_indicator,
        name="indicator",
    ),
    path(
        "celery-workers/",
        celery_workers,
        name="celery-workers",
    ),
    path(
        "tmux-processes/",
        tmux_processes,
        name="tmux-processes",
    ),
]
