import json

from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import (
    SendParticipantRecordingEmailParams,
    send_participant_recording_email,
)


@app.task(name="send_participant_recording_email", base=BaseTaskWithRetry)
def task_send_participant_recording_email(serialized_params: str):
    """Task for `send_participant_recording_email`"""
    send_participant_recording_email(
        SendParticipantRecordingEmailParams(**json.loads(serialized_params))
    )
