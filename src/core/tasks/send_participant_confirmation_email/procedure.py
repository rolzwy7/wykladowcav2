import json
from random import choice

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.eventlog import eventlog_participant_confirmation_email
from core.libs.notifications.email import (
    EmailMessage,
    EmailTemplate,
    email_get_application_context,
)


class SendParticipantConfirmationEmailParams(BaseModel):
    """Params"""

    email: str
    webinar_id: int
    application_id: int


def params(email: str, application_id: int, webinar_id: int) -> str:
    """Create params"""
    json_dump = json.dumps(
        SendParticipantConfirmationEmailParams(
            email=email, webinar_id=webinar_id, application_id=application_id
        ).dict()
    )
    return json_dump


def send_participant_confirmation_email(
    procedure_params: SendParticipantConfirmationEmailParams,
):
    """Send participant confirmation email after application has been sent"""
    email_template = EmailTemplate(
        "email/EmailParticipantConfirmation.html",
        email_get_application_context(procedure_params.application_id),
    )
    email_message = EmailMessage(
        email_template,
        choice(
            [
                "Zostali Państwo zapisani na szkolenie",
                "Zostali Państwo zapisani na szkolenie jako uczestnicy",
            ]
        ),
        procedure_params.email,
    )
    email_message.send()

    eventlog_participant_confirmation_email(
        procedure_params.webinar_id, procedure_params.email
    )
