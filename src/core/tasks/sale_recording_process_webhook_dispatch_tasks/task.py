# flake8: noqa=E501

from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import sale_recording_process_webhook_dispatch_tasks


@app.task(name="sale_recording_process_webhook_dispatch_tasks", base=BaseTaskWithRetry)
def task_sale_recording_process_webhook_dispatch_tasks(invoice_proforma_id: int):
    """Task for `sale_recording_process_webhook_dispatch_tasks`"""
    if invoice_proforma_id == 0:
        return "NO_PROFORMA"
    else:
        sale_recording_process_webhook_dispatch_tasks(invoice_proforma_id)
