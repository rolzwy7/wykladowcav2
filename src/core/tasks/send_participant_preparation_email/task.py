import json

from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import (
    SendParticipantPreparationEmailParams,
    send_participant_preparation_email,
)


@app.task(name="send_participant_preparation_email", base=BaseTaskWithRetry)
def task_send_participant_preparation_email(serialized_params: str):
    """Task for `send_participant_preparation_email`"""
    send_participant_preparation_email(
        SendParticipantPreparationEmailParams(**json.loads(serialized_params))
    )
