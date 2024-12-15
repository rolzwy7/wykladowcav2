"""
SendFreeParticipantConferenceEmail Task
"""

# flake8: noqa=E501

import json

from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import (
    SendFreeParticipantConferenceConfirmationEmailParams,
    send_free_participant_conference_confirmation_email,
)


@app.task(
    name="send_free_participant_conference_confirmation_email", base=BaseTaskWithRetry
)
def task_send_free_participant_conference_confirmation_email(serialized_params: str):
    """Task for `send_free_participant_conference_confirmation_email`"""
    send_free_participant_conference_confirmation_email(
        SendFreeParticipantConferenceConfirmationEmailParams(
            **json.loads(serialized_params)
        )
    )
