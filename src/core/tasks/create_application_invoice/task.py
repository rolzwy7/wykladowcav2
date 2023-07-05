import json

from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import create_application_invoice


@app.task(name="create_application_invoice", base=BaseTaskWithRetry)
def task_create_application_invoice(application_id: int):
    """Task for `create_application_invoice`"""
    return json.dumps(create_application_invoice(application_id).dict())
