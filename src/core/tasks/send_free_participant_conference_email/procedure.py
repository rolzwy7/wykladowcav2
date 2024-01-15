"""
SendFreeParticipantConferenceEmail Procedure
"""

import json

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.notifications.email import EmailMessage, EmailTemplate


class SendFreeParticipantConferenceEmailParams(BaseModel):
    """Params"""

    email: str
    conference_url: str


def params(email: str, conference_url: str) -> str:
    """Create params"""
    json_dump = json.dumps(
        SendFreeParticipantConferenceEmailParams(
            email=email, conference_url=conference_url
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
        },
    )
    email_message = EmailMessage(
        email_template,
        "Twoje zgłoszenie zostało przez nas przyjęte",
        procedure_params.email,
    )
    email_message.send()
