import requests
from django.conf import settings

TELEGRAM_API_BASE = settings.TELEGRAM_API_BASE
TELEGRAM_API_KEY = settings.TELEGRAM_API_KEY


class TelegramChats:
    """Chat IDs"""

    TELEGRAM_CHAT_ID_APPLICATIONS = settings.TELEGRAM_CHAT_ID_APPLICATIONS
    TELEGRAM_CHAT_ID_OTHER = settings.TELEGRAM_CHAT_ID_OTHER


class TelegramService:
    """Handles Telegram notifications"""

    def __init__(self) -> None:
        pass

    def send_chat_message(self, message: str, chat_id: str):
        """Send telegram chat message

        Args:
            message (str): message content
            chat_id (str): ID of target chat
        """
        url = f"{TELEGRAM_API_BASE}/bot{TELEGRAM_API_KEY}/sendMessage"
        response = requests.post(
            url,
            timeout=10,
            data={
                "chat_id": chat_id,
                "text": message,
            },
        )
        response.raise_for_status()
