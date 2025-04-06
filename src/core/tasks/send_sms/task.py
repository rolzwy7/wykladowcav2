from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import send_sms


@app.task(name="send_sms", base=BaseTaskWithRetry)
def task_send_sms(phone_number: str, message: str):
    """Task for `send_sms`"""
    send_sms(phone_number, message)
