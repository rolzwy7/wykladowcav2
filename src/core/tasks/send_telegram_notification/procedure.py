import requests
from django.conf import settings
from requests import Response

TELEGRAM_API_BASE = settings.TELEGRAM_API_BASE
TELEGRAM_API_KEY = settings.TELEGRAM_API_KEY


def send_telegram_notification(message: str, chat_id: str) -> Response:
    """Send telegram notification"""
    url = f"{TELEGRAM_API_BASE}/bot{TELEGRAM_API_KEY}/sendMessage"
    return requests.post(
        url,
        timeout=(10, 10),
        data={
            "chat_id": chat_id,
            "text": message,
        },
    )
