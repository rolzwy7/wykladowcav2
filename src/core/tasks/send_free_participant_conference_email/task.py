"""
SendFreeParticipantConferenceEmail Task
"""

# flake8: noqa=E501

import json

from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import (
    SendFreeParticipantConferenceEmailParams,
    send_free_participant_conference_email,
)


@app.task(name="send_free_participant_conference_email", base=BaseTaskWithRetry)
def task_send_free_participant_conference_email(serialized_params: str):
    """Task for `send_free_participant_conference_email`"""
    send_free_participant_conference_email(
        SendFreeParticipantConferenceEmailParams(**json.loads(serialized_params))
    )
