from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import create_participant_certificate


@app.task(name="create_participant_certificate", base=BaseTaskWithRetry)
def task_create_participant_certificate(participant_id: int) -> str:
    """Task for `create_participant_certificate`"""
    return create_participant_certificate(participant_id)
