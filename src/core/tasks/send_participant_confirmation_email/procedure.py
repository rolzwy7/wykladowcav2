import json

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.notifications.email import EmailMessage, EmailTemplate


class SendParticipantConfirmationEmailParams(BaseModel):
    """Params"""

    email: str


def params(email: str) -> str:
    """Create params"""
    json_dump = json.dumps(
        SendParticipantConfirmationEmailParams(email=email).dict()
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
