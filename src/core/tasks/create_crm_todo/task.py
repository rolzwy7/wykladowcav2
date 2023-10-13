from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import create_crm_todo


@app.task(name="create_crm_todo", base=BaseTaskWithRetry)
def task_create_crm_todo(message: str):
    """Task for `create_crm_todo`"""
    create_crm_todo(message)
