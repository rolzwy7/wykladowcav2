"""dispatch_opinion_requests"""

# flake8: noqa:E501
# pylint: disable=line-too-long
# pylint: disable=import-outside-toplevel

from celery import group

from core.consts.telegram_chats_consts import TelegramChats
from core.models import Webinar, WebinarParticipant
from core.tasks import (
    params_send_participant_opinion_email,
    task_send_participant_opinion_email,
    task_send_telegram_notification,
)


def dispatch_opinion_requests(webinar: Webinar):
    """dispatch_opinion_requests"""

    # Prepare data
    webinar_id: int = webinar.id  # type: ignore
    participants = WebinarParticipant.manager.get_valid_participants_for_webinar(
        webinar
    )

    # Create certificate jobs
    jobs = [
        task_send_participant_opinion_email.si(
            params_send_participant_opinion_email(
                participant.email, participant.application.id
            )
        )
        for participant in participants
    ]

    jobs.append(
        task_send_telegram_notification.si(
            f"Wysłano prośby o opinie dla szkolenia #{webinar_id}",
            TelegramChats.OTHER,
        ),
    )

    # Dispatch certificate tasks
    group(*jobs).apply_async()
