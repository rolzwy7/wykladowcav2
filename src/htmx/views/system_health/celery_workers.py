"""Health indicator"""

# pylint: disable=unused-variable
# pylint: disable=broad-exception-caught
# flake8: noqa=F841

from django.template.response import TemplateResponse
from django.utils.timezone import now

from core.services import HealthcheckService


def celery_workers(request):
    """Celery workers"""
    template_name = "htmx/system_health/celery_workers.html"

    healtcheck_service = HealthcheckService()

    try:
        workers = healtcheck_service.fetch_celery_workers()
    except Exception as e:
        workers = []

    return TemplateResponse(
        request,
        template_name,
        {"workers": workers, "checked_at": now()},
    )
