import json

from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import (
    SendParticipantConfirmationEmailParams,
    send_participant_confirmation_email,
)


@app.task(name="send_participant_confirmation_email", base=BaseTaskWithRetry)
def task_send_participant_confirmation_email(serialized_params: str):
    """Task for `send_participant_confirmation_email`"""
    send_participant_confirmation_email(
        SendParticipantConfirmationEmailParams(**json.loads(serialized_params))
    )
