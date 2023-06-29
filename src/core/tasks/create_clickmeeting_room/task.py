import json

from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import CreateClickmeetingRoomParams, create_clickmeeting_room


@app.task(name="create_clickmeeting_room", base=BaseTaskWithRetry)
def task_create_clickmeeting_room(serialized_params: str):
    """Task for `create_clickmeeting_room`"""
    create_clickmeeting_room(
        CreateClickmeetingRoomParams(**json.loads(serialized_params))
    )
