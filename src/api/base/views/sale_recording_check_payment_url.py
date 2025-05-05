"""
Fakturownia Webhook
"""

# flake8: noqa=E501

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from core.models import SaleRecordingApplication


@api_view(["GET"])
@renderer_classes([JSONRenderer])  # policy decorator
@permission_classes([AllowAny])  # Allow access without authentication
def sale_recording_check_payment_url(request, uuid):
    """sale_recording_check_payment_url"""

    application = SaleRecordingApplication.manager.get(uuid=uuid)

    return Response(
        {"payment_url": application.fakturownia_payment_url},
        status=status.HTTP_200_OK,
    )
