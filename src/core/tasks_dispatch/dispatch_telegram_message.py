# flake8: noqa:E501
# pylint: disable=line-too-long

from core.consts import TelegramChats
from core.tasks import task_send_telegram_notification


def dispatch_telegram_message(message: str, chat: str):
    """Dispatch telegram message for OTHER chat"""

    task_send_telegram_notification.si(
        message,
        chat,
    ).apply_async()
