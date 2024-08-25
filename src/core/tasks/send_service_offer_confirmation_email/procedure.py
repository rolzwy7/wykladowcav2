import json
from random import choice

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.notifications.email import EmailMessage, EmailTemplate


class SendServiceOfferConfirmationEmailParams(BaseModel):
    """Params"""

    email: str
    service_name: str


def params(email: str, service_name: str) -> str:
    """Create params"""
    json_dump = json.dumps(
        SendServiceOfferConfirmationEmailParams(
            email=email, service_name=service_name
        ).dict()
    )
    return json_dump


def send_service_offer_confirmation_email(
    procedure_params: SendServiceOfferConfirmationEmailParams,
):
    """Send submitter confirmation email after application has been sent"""
    email_template = EmailTemplate(
        "email/EmailServiceOfferConfirmation.html",
        {"service_name": procedure_params.service_name},
    )
    email_message = EmailMessage(
        email_template,
        choice(["Otrzymaliśmy Państwa zapytanie ofertowe"]),
        procedure_params.email,
    )
    email_message.send()
