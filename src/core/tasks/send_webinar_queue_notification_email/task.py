import json

from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import (
    SendWebinarQueueNotificationEmailParams,
    send_webinar_queue_notification_email,
)


@app.task(name="send_webinar_queue_notification_email", base=BaseTaskWithRetry)
def task_send_webinar_queue_notification_email(serialized_params: str):
    """Task for `send_webinar_queue_notification_email`"""
    send_webinar_queue_notification_email(
        SendWebinarQueueNotificationEmailParams(**json.loads(serialized_params))
    )
