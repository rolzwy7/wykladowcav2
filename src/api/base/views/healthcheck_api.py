"""Healthcheck API"""

# flake8: noqa=E501

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from core.services import HealthcheckService


@api_view(["GET"])
@renderer_classes([JSONRenderer])  # policy decorator
def health_check(request: Request) -> Response:
    """Return company data from REGON"""

    healtcheck_service = HealthcheckService()
    workers = healtcheck_service.fetch_celery_workers()

    return Response(
        {
            "celery_workers": workers,
        }
    )
