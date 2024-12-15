"""
Procedure that executes after webinar application has been sent
"""

# flake8: noqa=E501

from celery import chain
from django.template.defaultfilters import date as _date
from django.urls import reverse
from django.utils.timezone import get_default_timezone

from core.consts import TelegramChats
from core.models import ConferenceEdition, ConferenceFreeParticipant, Webinar
from core.tasks import (
    params_send_free_participant_conference_email,
    task_send_free_participant_conference_email,
    task_send_telegram_notification,
)


def after_free_conference_participant_singup(
    edition: ConferenceEdition,
    participant: ConferenceFreeParticipant,
):
    """Dispatch tasks after free conference participant singup"""

    tz = get_default_timezone()
    webinar: Webinar = edition.webinar
    webinar_date = webinar.date

    chain(
        # Send e-mail with conference URL
        task_send_free_participant_conference_email.si(
            params_send_free_participant_conference_email(
                webinar.title,
                participant.email,
                reverse(
                    "core:conference_waiting_room_page",
                    kwargs={
                        "watch_token": str(participant.watch_token),
                    },
                ),
                _date(webinar_date.astimezone(tz), "j E Y"),
                _date(webinar_date.astimezone(tz), "H:i"),
            )
        ),
        # Send telegram notification
        task_send_telegram_notification.si(
            f"Darmowy uczestnik ({participant.email}) zapisał się na szkolenie: {webinar.title}",
            TelegramChats.OTHER,
        ),
    ).apply_async()
