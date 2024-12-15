# flake8: noqa:E501
# pylint: disable=line-too-long

from celery import chain, group
from django.template.defaultfilters import date as _date
from django.urls import reverse
from django.utils.timezone import get_default_timezone

from core.consts import TelegramChats
from core.models import (
    ConferenceEdition,
    ConferenceFreeParticipant,
    Lecturer,
    Webinar,
    WebinarMetadata,
    WebinarParticipant,
)
from core.tasks import (
    params_create_clickmeeting_room,
    params_send_free_participant_conference_confirmation_email,
    params_send_free_participant_conference_email,
    params_send_participant_preparation_email,
    task_create_clickmeeting_room,
    task_send_clickmeeting_invitation_lecturer,
    task_send_clickmeeting_invitation_participant,
    task_send_free_participant_conference_confirmation_email,
    task_send_free_participant_conference_email,
    task_send_participant_preparation_email,
    task_send_telegram_notification,
)


def after_conference_confirm_dispatch(edition: ConferenceEdition):
    """after_conference_confirm_dispatch"""

    # Prepare data
    tz = get_default_timezone()
    webinar: Webinar = edition.webinar
    webinar_date = webinar.date

    free_participants = ConferenceFreeParticipant.manager.filter(edition=edition)
    free_participants_count = free_participants.count()

    free_participants_confirmations = [
        task_send_free_participant_conference_confirmation_email.si(
            params_send_free_participant_conference_confirmation_email(
                webinar.title,
                free_participant.email,
                reverse(
                    "core:conference_waiting_room_page",
                    kwargs={
                        "watch_token": str(free_participant.watch_token),
                    },
                ),
                _date(webinar_date.astimezone(tz), "j E Y"),
                _date(webinar_date.astimezone(tz), "H:i"),
            )
        )
        for free_participant in free_participants
    ]

    chain(
        # Send confirmation e-mails with conference URL
        group(*free_participants_confirmations),
        # Send telegram notification
        task_send_telegram_notification.si(
            f"Wysłano przypomnienia do {free_participants_count} uczestników"
            f" darmowego szkolenia {webinar.title}",
            TelegramChats.OTHER,
        ),
    ).apply_async()
