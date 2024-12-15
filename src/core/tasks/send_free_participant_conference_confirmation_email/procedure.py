"""
SendFreeParticipantConferenceEmail Procedure
"""

# flake8: noqa=E501
import json
from random import choice

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.notifications.email import EmailMessage, EmailTemplate


class SendFreeParticipantConferenceConfirmationEmailParams(BaseModel):
    """Params"""

    webinar_title: str
    email: str
    conference_url: str
    start_date: str
    start_hour: str


def params(
    webinar_title: str,
    email: str,
    conference_url: str,
    start_date: str,
    start_hour: str,
) -> str:
    """Create params"""
    json_dump = json.dumps(
        SendFreeParticipantConferenceConfirmationEmailParams(
            webinar_title=webinar_title,
            email=email,
            conference_url=conference_url,
            start_date=start_date,
            start_hour=start_hour,
        ).dict()
    )
    return json_dump


def send_free_participant_conference_confirmation_email(
    procedure_params: SendFreeParticipantConferenceConfirmationEmailParams,
):
    """Send participant confirmation email"""
    email_template = EmailTemplate(
        "email/EmailFreeParticipantConferenceConfirmation.html",
        {
            "webinar_title": procedure_params.webinar_title,
            "conference_url": procedure_params.conference_url,
            "start_date": procedure_params.start_date,
            "start_hour": procedure_params.start_hour,
        },
    )
    email_message = EmailMessage(
        email_template,
        choice(["Przypomnienie o bezpłatnym szkoleniu"]),
        procedure_params.email,
    )
    email_message.send()
