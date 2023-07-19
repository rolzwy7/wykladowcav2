import json

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.eventlog import eventlog_submitter_confirmation_email
from core.libs.notifications.email import (
    EmailMessage,
    EmailTemplate,
    email_get_application_context,
)


class SendSubmitterMovingEmailParams(BaseModel):
    """Params"""

    email: str
    webinar_id: int
    application_id: int


def params(email: str, webinar_id: int, application_id: int) -> str:
    """Create params"""
    json_dump = json.dumps(
        SendSubmitterMovingEmailParams(
            email=email, webinar_id=webinar_id, application_id=application_id
        ).dict()
    )
    return json_dump


def send_submitter_moving_email(
    procedure_params: SendSubmitterMovingEmailParams,
):
    """Send submitter confirmation email after application has been sent"""
    email_template = EmailTemplate(
        "email/EmailSubmitterMoving.html",
        email_get_application_context(procedure_params.application_id),
    )
    email_message = EmailMessage(
        email_template,
        "Ważne informacje o szkoleniu 19.07.2023 ",
        procedure_params.email,
    )
    email_message.send()

    eventlog_submitter_confirmation_email(
        procedure_params.webinar_id, procedure_params.email
    )
