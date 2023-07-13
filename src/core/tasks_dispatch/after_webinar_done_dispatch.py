# flake8: noqa:E501
# pylint: disable=line-too-long
import json
from datetime import timedelta

from celery import chain, group
from django.utils.timezone import now
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from core.models import Webinar, WebinarApplication, WebinarParticipant
from core.tasks import (
    params_send_participant_certificate_email,
    params_send_participant_opinion_email,
    task_create_application_invoice,
    task_create_participant_certificate,
    task_save_application_invoice_metadata,
    task_send_invoice_email,
    task_send_participant_certificate_email,
    task_send_telegram_notification,
)


def after_webinar_done_dispatch(webinar: Webinar):
    """Performs actions after webinar is done"""

    webinar_id: int = webinar.id  # type: ignore

    # Create "every 35 minutes" interval
    schedule_35m, _ = IntervalSchedule.objects.get_or_create(
        every=35,
        period=IntervalSchedule.MINUTES,
    )

    # Create "every 24 hours" interval
    schedule_24h, _ = IntervalSchedule.objects.get_or_create(
        every=24,
        period=IntervalSchedule.HOURS,
    )

    # Prepare data
    participants = (
        WebinarParticipant.manager.get_participants_from_sent_applications(
            webinar
        )
    )
    applications = WebinarApplication.manager.sent_applications(webinar)

    invoice_jobs = [
        chain(
            task_create_application_invoice.si(application.id),  # type: ignore
            task_save_application_invoice_metadata.s(application.id),  # type: ignore
            task_send_invoice_email.si(application.invoice.invoice_email, application.id),  # type: ignore
        )
        for application in applications
    ]

    certificate_jobs = [
        chain(
            task_create_participant_certificate.si(participant.id),  # type: ignore
            # Passes certificate URL to next task
            task_send_participant_certificate_email.s(
                # certificate_url passed here,
                params_send_participant_certificate_email(
                    participant.email,
                    participant.application.webinar,
                )
            ),
        )
        for participant in participants
    ]

    chain(
        # Create invoices
        group(*invoice_jobs),
        # Create and send certificates
        group(*certificate_jobs),
        # Send Telegram notification
        task_send_telegram_notification.si(
            f"Zrealizowano szkolenie #{webinar_id}"
        ),
    ).apply_async()

    # Schedule periodic task: download recording
    PeriodicTask.objects.create(
        interval=schedule_35m,
        name=f"Downloading clickmeeting recording for webinar #{webinar_id}",
        task="download_and_process_clickmeeting_recording",
        args=json.dumps([webinar_id]),
        expires=now()
        + timedelta(hours=24),  # try to download within 24h or give up
    )

    # Schedule periodic task: Send opinion e-mail
    for participant in participants:
        participant_id: int = participant.id  # type: ignore
        PeriodicTask.objects.create(
            interval=schedule_24h,
            one_off=True,
            name=f"Send opinion e-mail to participant #{participant_id}",
            task="send_participant_opinion_email",
            args=params_send_participant_opinion_email(
                participant.email, webinar
            ),
            expires=now()
            + timedelta(hours=30),  # just in case to prevent resend
        )
