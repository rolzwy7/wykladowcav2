import json

from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import CreateEventlogParams, create_eventlog


@app.task(name="create_webinar_eventlog", base=BaseTaskWithRetry)
def task_create_eventlog(serialized_params: str):
    """Task for `create_webinar_eventlog`"""
    create_eventlog(CreateEventlogParams(**json.loads(serialized_params)))
