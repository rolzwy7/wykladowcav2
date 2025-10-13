"""
Fakturownia Webhook
"""

# flake8: noqa=E501

from celery import chain
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from core.consts import TelegramChats
from core.services import TelegramService
from core.tasks import (
    params_sale_recording_process_webhook,
    task_sale_recording_process_webhook,
    task_sale_recording_process_webhook_dispatch_tasks,
    task_send_telegram_notification,
)


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
        f"fakturownia_sale_recording_webhook webhook:\n\n{data}",
        TelegramChats.DEBUG,
    )

    if api_token != "DO6TPnB6J73IAEn":
        return Response(
            {"error": "Nieprawidłowy api_token"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Skip invoice with 'kind'='proforma'
    kind = data["deal"]["kind"]
    if kind == "proforma":
        return Response(
            {"message": "SUCCESS: Skipping Proforma"},
            status=status.HTTP_200_OK,
        )

    # Get VAT invoice ID
    invoice_vat_id = int(data["id"])

    chain(
        task_sale_recording_process_webhook.si(
            params_sale_recording_process_webhook(invoice_vat_id)
        ),
        task_sale_recording_process_webhook_dispatch_tasks.s(),
        task_send_telegram_notification.si(
            f"Zakończono procedure po płatności. Faktura id={invoice_vat_id}",
            TelegramChats.DEBUG,
        ),
    ).apply_async()

    # Return a success response
    return Response(
        {"message": "SUCCESS"},
        status=status.HTTP_200_OK,
    )
