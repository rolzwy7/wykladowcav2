import json

from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import CreateWebinarEventlogParams, create_webinar_eventlog


@app.task(name="create_webinar_eventlog", base=BaseTaskWithRetry)
def task_create_webinar_eventlog(serialized_params: str):
    """Task for `create_webinar_eventlog`"""
    create_webinar_eventlog(
        CreateWebinarEventlogParams(**json.loads(serialized_params))
    )
