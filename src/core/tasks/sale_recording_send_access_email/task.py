# flake8: noqa=E501

import json

from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import (
    SaleRecordingSendAccessEmailParams,
    sale_recording_send_access_email,
)


@app.task(name="sale_recording_send_access_email", base=BaseTaskWithRetry)
def task_sale_recording_send_access_email(access_url: str, serialized_params: str):
    """Task for `sale_recording_send_access_email`"""
    sale_recording_send_access_email(
        access_url,
        SaleRecordingSendAccessEmailParams(**json.loads(serialized_params)),
    )
