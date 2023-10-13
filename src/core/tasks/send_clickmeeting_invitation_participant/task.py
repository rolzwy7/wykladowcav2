from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import send_clickmeeting_invitation_participant


@app.task(
    name="send_clickmeeting_invitation_participant", base=BaseTaskWithRetry
)
def task_send_clickmeeting_invitation_participant(room_id: int, email: str):
    """Task for `send_clickmeeting_invitation_participant`"""
    return send_clickmeeting_invitation_participant(room_id, email)
