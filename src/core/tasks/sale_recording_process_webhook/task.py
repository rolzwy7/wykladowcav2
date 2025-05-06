# flake8: noqa=E501

import json

from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import SaleRecordingProcessWebhookParams, sale_recording_process_webhook


@app.task(name="sale_recording_process_webhook", base=BaseTaskWithRetry)
def task_sale_recording_process_webhook(serialized_params: str):
    """Task for `sale_recording_process_webhook`"""
    return sale_recording_process_webhook(
        SaleRecordingProcessWebhookParams(**json.loads(serialized_params)),
    )
