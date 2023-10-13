from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import send_clickmeeting_invitation_lecturer


@app.task(name="send_clickmeeting_invitation_lecturer", base=BaseTaskWithRetry)
def task_send_clickmeeting_invitation_lecturer(room_id: int, email: str):
    """Task for `send_clickmeeting_invitation_lecturer`"""
    return send_clickmeeting_invitation_lecturer(room_id, email)
