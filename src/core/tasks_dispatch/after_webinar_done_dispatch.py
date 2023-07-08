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
    task_send_participant_certificate_email,
    task_send_participant_opinion_email,
)


def after_webinar_done_dispatch(webinar: Webinar):
    """Performs actions after webinar is done"""

    webinar_id: int = webinar.id  # type: ignore

    # Schedule periodic tasks
    # Create "every 35 minutes" interval
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=35,
        period=IntervalSchedule.MINUTES,
    )

    # Download recording periodict task
    PeriodicTask.objects.create(
        interval=schedule,
        name=f"Downloading clickmeeting recording for webinar ID={webinar_id}",
        task="download_and_process_clickmeeting_recording",
        args=json.dumps([webinar_id]),
        expires=now() + timedelta(days=1),
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
            # TODO: Send invoice via e-mail
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

    opinion_jobs = [
        task_send_participant_opinion_email.si(
            params_send_participant_opinion_email(participant.email, webinar)
        )
        for participant in participants
    ]

    chain(
        # Create invoices
        group(*invoice_jobs),
        # Create and send certificates
        group(*certificate_jobs),
        # Queue opinion emails
        group(*opinion_jobs),
    ).apply_async()
