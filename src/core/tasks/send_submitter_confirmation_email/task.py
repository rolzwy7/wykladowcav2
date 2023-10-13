import json

from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import (
    SendSubmitterConfirmationEmailParams,
    send_submitter_confirmation_email,
)


@app.task(name="send_submitter_confirmation_email", base=BaseTaskWithRetry)
def task_send_submitter_confirmation_email(serialized_params: str):
    """Task for `send_submitter_confirmation_email`"""
    send_submitter_confirmation_email(
        SendSubmitterConfirmationEmailParams(**json.loads(serialized_params))
    )
