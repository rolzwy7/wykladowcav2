import json

from django.template.defaultfilters import date as _date
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.notifications.email import (
    EmailMessage,
    EmailTemplate,
    email_get_application_context,
)
from core.models import Webinar, WebinarMoveRegister


class SendSubmitterMovingEmailParams(BaseModel):
    """Params"""

    email: str
    application_id: int
    move_register_id: int
    token: str


def params(
    email: str, application_id: int, move_register_id: int, token: str
) -> str:
    """Create params"""
    json_dump = json.dumps(
        SendSubmitterMovingEmailParams(
            email=email,
            application_id=application_id,
            move_register_id=move_register_id,
            token=token,
        ).dict()
    )
    return json_dump


def send_submitter_moving_email(
    procedure_params: SendSubmitterMovingEmailParams,
):
    """Send submitter confirmation email after application has been sent"""
    move_register: WebinarMoveRegister = WebinarMoveRegister.manager.get(
        id=procedure_params.move_register_id
    )
    email_context = email_get_application_context(
        procedure_params.application_id
    )
    email_template = EmailTemplate(
        "email/EmailSubmitterMoving.html",
        {
            **email_context,
            "new_date": move_register.to_datetime,
            "old_date": move_register.from_datetime,
            "token": procedure_params.token,
        },
    )

    webinar: Webinar = email_context["webinar"]
    webinar_date = _date(webinar.date, "j E Y")

    email_message = EmailMessage(
        email_template,
        f"Ważne informacje o szkoleniu {webinar_date}",
        procedure_params.email,
    )
    email_message.send()
