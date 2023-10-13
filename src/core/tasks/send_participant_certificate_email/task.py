import json

from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import (
    SendParticipantCertificateEmailParams,
    send_participant_certificate_email,
)


@app.task(name="send_participant_certificate_email", base=BaseTaskWithRetry)
def task_send_participant_certificate_email(
    certificate_url: str, serialized_params: str
):
    """Task for `send_participant_certificate_email`"""
    send_participant_certificate_email(
        certificate_url,
        SendParticipantCertificateEmailParams(**json.loads(serialized_params)),
    )
