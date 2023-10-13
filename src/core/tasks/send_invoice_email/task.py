from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import send_invoice_email


@app.task(name="send_invoice_email", base=BaseTaskWithRetry)
def task_send_invoice_email(email: str, application_id: int):
    """Task for `send_invoice_email`"""
    send_invoice_email(email, application_id)
