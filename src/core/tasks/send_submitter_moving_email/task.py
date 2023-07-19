import json

from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import (
    SendSubmitterMovingEmailParams,
    send_submitter_moving_email,
)


@app.task(name="send_submitter_moving_email", base=BaseTaskWithRetry)
def task_send_submitter_moving_email(serialized_params: str):
    """Task for `send_submitter_moving_email`"""
    send_submitter_moving_email(
        SendSubmitterMovingEmailParams(**json.loads(serialized_params))
    )
