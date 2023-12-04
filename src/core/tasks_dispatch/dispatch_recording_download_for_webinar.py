# flake8: noqa:E501
# pylint: disable=line-too-long
# pylint: disable=import-outside-toplevel
import json
from datetime import timedelta

from django.utils.timezone import now
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from core.models import Webinar


def dispatch_recording_download_for_webinar(webinar: Webinar):
    """Dispatch recording download for given webinar"""

    # Prepare intervals
    # Create "every 35 minutes" interval
    schedule_35m, _ = IntervalSchedule.objects.get_or_create(
        every=35,
        period=IntervalSchedule.MINUTES,
    )

    webinar_id: int = webinar.id  # type: ignore

    # Schedule periodic task: download recording
    # Try to download within 24h or give up
    PeriodicTask.objects.create(
        interval=schedule_35m,
        name=f"Downloading clickmeeting recording for webinar #{webinar_id}",
        task="download_and_process_clickmeeting_recording",
        args=json.dumps([webinar_id]),
        expires=now() + timedelta(hours=24),
    )
