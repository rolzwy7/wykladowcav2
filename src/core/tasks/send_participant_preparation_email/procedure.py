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


def params(email: str, application_id: int) -> str:
    """Create params"""
    json_dump = json.dumps(
        SendParticipantPreparationEmailParams(
            email=email, application_id=application_id
        ).dict()
    )
    return json_dump


def send_participant_preparation_email(
    procedure_params: SendParticipantPreparationEmailParams,
):
    """Send participant confirmation email after application has been sent"""
    email_template = EmailTemplate(
        "email/EmailParticipantPreparation.html",
        {**email_get_application_context(procedure_params.application_id)},
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

    # TODO: eventlog_participant_confirmation_email(
    #     procedure_params.webinar_id, procedure_params.email
    # )
