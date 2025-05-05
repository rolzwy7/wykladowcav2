"""
Fakturownia Webhook
"""

# flake8: noqa=E501

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from core.consts import TelegramChats
from core.services import TelegramService


@api_view(["POST"])
@renderer_classes([JSONRenderer])  # policy decorator
@permission_classes([AllowAny])  # Allow access without authentication
def fakturownia_sale_recording_webhook(request):
    """fakturownia_sale_recording_webhook"""

    # Extract JSON data from the request
    data = request.data
    api_token = data.get("api_token", "no_token")

    telegram_service = TelegramService()
    telegram_service.try_send_chat_message(
        f"Fakturownia webhook:\n\n{data}",
        TelegramChats.OTHER,
    )

    if api_token != "DO6TPnB6J73IAEn":
        return Response(
            {"error": "Nieprawidłowy api_token"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Return a success response
    return Response(
        {"message": "Webhook received and processed successfully"},
        status=status.HTTP_200_OK,
    )
