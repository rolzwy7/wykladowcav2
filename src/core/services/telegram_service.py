import requests
from django.conf import settings
from requests import Response

TELEGRAM_API_BASE = settings.TELEGRAM_API_BASE
TELEGRAM_API_KEY = settings.TELEGRAM_API_KEY
APP_ENV = settings.APP_ENV


class TelegramService:
    """Handles Telegram notifications"""

    def __init__(self) -> None:
        pass

    def send_chat_message(self, message: str, chat_id: str) -> Response:
        """Send telegram chat message

        Args:
            message (str): message content
            chat_id (str): ID of target chat
        """
        url = f"{TELEGRAM_API_BASE}/bot{TELEGRAM_API_KEY}/sendMessage"

        if APP_ENV == "develop":
            message = f"[TEST] {message}"

        response = requests.post(
            url,
            timeout=10,
            data={
                "chat_id": chat_id,
                "text": message,
            },
        )
        response.raise_for_status()
        return response
