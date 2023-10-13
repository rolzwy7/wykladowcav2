from requests import Response

from core.services import TelegramService


def send_telegram_notification(message: str, chat_id: str) -> Response:
    """Send telegram notification"""

    telegram_service = TelegramService()
    return telegram_service.send_chat_message(message, chat_id)
