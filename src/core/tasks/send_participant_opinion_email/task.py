import json

from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import (
    SendParticipantOpinionEmailParams,
    send_participant_opinion_email,
)


@app.task(name="send_participant_opinion_email", base=BaseTaskWithRetry)
def task_send_participant_opinion_email(serialized_params: str):
    """Task for `send_participant_opinion_email`"""
    send_participant_opinion_email(
        SendParticipantOpinionEmailParams(**json.loads(serialized_params))
    )
