"""task for sale_recording_create_application_invoice"""

# flake8: noqa

import json

from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import sale_recording_create_application_invoice


@app.task(name="sale_recording_create_application_invoice", base=BaseTaskWithRetry)
def task_sale_recording_create_application_invoice(application_id: int):
    """Task for `sale_recording_create_application_invoice`"""
    return json.dumps(sale_recording_create_application_invoice(application_id).dict())
