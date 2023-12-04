# flake8: noqa:E501
# pylint: disable=line-too-long
# pylint: disable=import-outside-toplevel

from celery import chain, group

from core.models import Webinar, WebinarParticipant
from core.tasks import (
    params_send_participant_certificate_email,
    task_create_participant_certificate,
    task_send_participant_certificate_email,
)


def dispatch_certificates_for_webinar(webinar: Webinar):
    """Dispatch certificates for given webinar"""

    # Prepare data
    participants = WebinarParticipant.manager.get_valid_participants_for_webinar(
        webinar
    )

    # Create certificate jobs
    certificate_jobs = [
        chain(
            task_create_participant_certificate.si(participant.id),  # type: ignore
            # Passes certificate URL to next task
            task_send_participant_certificate_email.s(
                # certificate_url passed here,
                params_send_participant_certificate_email(
                    participant.email,
                    participant.application.id,
                )
            ),
        )
        for participant in participants
    ]

    # Dispatch certificate tasks
    group(*certificate_jobs).apply_async()
