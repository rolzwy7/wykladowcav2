from celery import chain

from core.models import Webinar
from core.tasks import (
    params_create_clickmeeting_room,
    task_create_clickmeeting_room,
)


def after_webinar_confirm(webinar: Webinar):
    """Performs actions after webinar confirmation"""
    create_clickmeeting_job = task_create_clickmeeting_room.s(
        params_create_clickmeeting_room(webinar)
    )

    chain(create_clickmeeting_job).apply_async()
