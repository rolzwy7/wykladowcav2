"""
Procedure that executes after webinar application has been sent
"""

# flake8: noqa=E501

from celery import chain
from django.urls import reverse

from core.consts import TelegramChats
from core.models import ConferenceEdition, ConferenceFreeParticipant
from core.tasks import (
    params_send_free_participant_conference_email,
    task_send_clickmeeting_invitation_participant,
    task_send_free_participant_conference_email,
    task_send_telegram_notification,
)


def after_free_conference_participant_singup(
    edition: ConferenceEdition,
    participant: ConferenceFreeParticipant,
):
    """Dispatch tasks after free conference participant singup"""

    chain(
        # Send clickmeeting invite to free participant
        task_send_clickmeeting_invitation_participant.si(
            edition.clickmeeting_id, participant.email
        ),
        # Send e-mail with conference URL
        task_send_free_participant_conference_email.si(
            params_send_free_participant_conference_email(
                participant.email,
                reverse(
                    "core:conference_edition_redirect_page",
                    kwargs={
                        "uuid": edition.redirect_token,
                    },
                ),
            )
        ),
        # Send telegram notification
        task_send_telegram_notification.si(
            f"Darmowy uczestnik zapisał się na szkolenie: {edition.webinar.title}",
            TelegramChats.OTHER,
        ),
    ).apply_async()
