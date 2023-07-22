import json

from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import (
    SendSubmitterCancellationEmailParams,
    send_submitter_cancellation_email,
)


@app.task(name="send_submitter_cancellation_email", base=BaseTaskWithRetry)
def task_send_submitter_cancellation_email(serialized_params: str):
    """Task for `send_submitter_cancellation_email`"""
    send_submitter_cancellation_email(
        SendSubmitterCancellationEmailParams(**json.loads(serialized_params))
    )
