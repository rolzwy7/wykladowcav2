import json

from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import CreateClickmeetingRoomParams, create_clickmeeting_room


@app.task(name="create_clickmeeting_room", base=BaseTaskWithRetry)
def task_create_clickmeeting_room(serialized_params: str) -> int:
    """Task for `create_clickmeeting_room`

    Args:
        serialized_params (str): serialized data

    Returns:
        int: Clickmeeting room ID
    """
    room_id = create_clickmeeting_room(
        CreateClickmeetingRoomParams(**json.loads(serialized_params))
    )
    return room_id
