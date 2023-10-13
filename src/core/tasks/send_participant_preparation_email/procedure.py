import json
from random import choice

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.notifications.email import (
    EmailMessage,
    EmailTemplate,
    email_get_application_context,
)


class SendParticipantPreparationEmailParams(BaseModel):
    """Params"""

    application_id: int
    email: str
    assets_url: str


def params(email: str, application_id: int, assets_url: str) -> str:
    """Create params"""
    json_dump = json.dumps(
        SendParticipantPreparationEmailParams(
            email=email, application_id=application_id, assets_url=assets_url
        ).dict()
    )
    return json_dump


def send_participant_preparation_email(
    procedure_params: SendParticipantPreparationEmailParams,
):
    """Send participant confirmation email after application has been sent"""
    email_template = EmailTemplate(
        "email/EmailParticipantPreparation.html",
        {
            **email_get_application_context(procedure_params.application_id),
            "assets_url": procedure_params.assets_url,
        },
    )
    email_message = EmailMessage(
        email_template,
        choice(
            [
                "Potwierdzamy termin szkolenia",
                "Termin szkolenia został potwierdzony",
            ]
        ),
        procedure_params.email,
    )
    email_message.send()
