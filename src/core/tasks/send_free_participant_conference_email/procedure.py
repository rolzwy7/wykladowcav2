"""
SendFreeParticipantConferenceEmail Procedure
"""

# flake8: noqa=E501
import json
from random import choice

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.notifications.email import EmailMessage, EmailTemplate


class SendFreeParticipantConferenceEmailParams(BaseModel):
    """Params"""

    email: str
    conference_url: str
    start_date: str
    start_hour: str


def params(email: str, conference_url: str, start_date: str, start_hour: str) -> str:
    """Create params"""
    json_dump = json.dumps(
        SendFreeParticipantConferenceEmailParams(
            email=email,
            conference_url=conference_url,
            start_date=start_date,
            start_hour=start_hour,
        ).dict()
    )
    return json_dump


def send_free_participant_conference_email(
    procedure_params: SendFreeParticipantConferenceEmailParams,
):
    """Send participant confirmation email after application has been sent"""
    email_template = EmailTemplate(
        "email/EmailFreeParticipantConference.html",
        {
            "conference_url": procedure_params.conference_url,
            "start_date": procedure_params.start_date,
            "start_hour": procedure_params.start_hour,
        },
    )
    email_message = EmailMessage(
        email_template,
        choice(
            [
                "Twoje zgłoszenie na szkolenie zostało przez nas przyjęte",
                "Przyjęliśmy Twoje zgłoszenie na szkolenie",
            ]
        ),
        procedure_params.email,
    )
    email_message.send()
