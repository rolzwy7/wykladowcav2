from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import download_and_process_clickmeeting_recording


@app.task(
    name="download_and_process_clickmeeting_recording", base=BaseTaskWithRetry
)
def task_download_and_process_clickmeeting_recording(webinar_id: int):
    """Task for `download_and_process_clickmeeting_recording`"""
    return download_and_process_clickmeeting_recording(webinar_id)
