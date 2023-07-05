import json

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.eventlog import eventlog_participant_confirmation_email
from core.libs.notifications.email import EmailMessage, EmailTemplate


class SendParticipantConfirmationEmailParams(BaseModel):
    """Params"""

    webinar_id: int
    email: str


def params(email: str, webinar_id: int) -> str:
    """Create params"""
    json_dump = json.dumps(
        SendParticipantConfirmationEmailParams(
            webinar_id=webinar_id, email=email
        ).dict()
    )
    return json_dump


def send_participant_confirmation_email(
    procedure_params: SendParticipantConfirmationEmailParams,
):
    """Send participant confirmation email after application has been sent"""
    email_template = EmailTemplate(
        "email/EmailParticipantConfirmation.html", {}
    )
    email_message = EmailMessage(
        email_template,
        "Zostali Państwo zapisani na szkolenie",
        procedure_params.email,
    )
    email_message.send()

    eventlog_participant_confirmation_email(
        procedure_params.webinar_id, procedure_params.email
    )
