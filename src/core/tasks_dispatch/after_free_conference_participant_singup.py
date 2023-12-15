"""
Procedure that executes after webinar application has been sent
"""

# flake8: noqa=E501

from celery import chain

from core.consts import TelegramChats
from core.models import ConferenceCycle, ConferenceEdition, ConferenceFreeParticipant
from core.tasks import (
    task_send_clickmeeting_invitation_participant,
    task_send_telegram_notification,
)


def after_free_conference_participant_singup(
    cycle: ConferenceCycle,
    edition: ConferenceEdition,
    participant: ConferenceFreeParticipant,
):
    """Dispatch tasks after free conference participant singup"""

    chain(
        # Send clickmeeting invite to free participant
        task_send_clickmeeting_invitation_participant.si(
            edition.clickmeeting_id, participant.email
        ),
        # Send telegram notification
        task_send_telegram_notification.si(
            f"Darmowy uczestnik zapisał się na szkolenie cykliczne: {cycle.name}",
            TelegramChats.OTHER,
        ),
    ).apply_async()
