import json

from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import (
    SendSaleRecordingOrderEmailParams,
    send_sale_recording_order_email,
)


@app.task(name="send_sale_recording_order_email", base=BaseTaskWithRetry)
def task_send_sale_recording_order_email(serialized_params: str):
    """Task for `send_sale_recording_order_email`"""
    send_sale_recording_order_email(
        SendSaleRecordingOrderEmailParams(**json.loads(serialized_params))
    )
