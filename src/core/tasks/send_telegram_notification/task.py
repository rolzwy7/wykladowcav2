from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import send_telegram_notification


@app.task(name="send_telegram_notification", base=BaseTaskWithRetry)
def task_send_telegram_notification(message: str, chat_id: str):
    """Task for `send_telegram_notification`"""
    send_telegram_notification(message, chat_id)
