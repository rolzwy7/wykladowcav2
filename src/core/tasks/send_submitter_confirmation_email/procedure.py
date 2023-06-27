import json

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.notifications.email import EmailMessage, EmailTemplate


class SendSubmitterConfirmationEmailParams(BaseModel):
    """Params"""

    email: str


def create_params(email: str) -> list[str]:
    """Create params"""
    json_dump = json.dumps(
        SendSubmitterConfirmationEmailParams(email=email).dict()
    )
    return [json_dump]


def send_submitter_confirmation_email(
    params: SendSubmitterConfirmationEmailParams,
):
    """Send submitter confirmation email after application has been sent"""
    email_template = EmailTemplate("email/EmailSubmitterConfirmation.html", {})
    email_message = EmailMessage(
        email_template,
        "Potwierdzamy otrzymanie zgłoszenia na szkolenie",
        params.email,
    )
    email_message.send()
