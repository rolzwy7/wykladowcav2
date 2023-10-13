import json

from django.conf import settings
from django.template.defaultfilters import date as _date
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.notifications.email import (
    EmailMessage,
    EmailTemplate,
    email_get_application_context,
)
from core.models import Webinar

BASE_URL = settings.BASE_URL


class SendSubmitterCancellationEmailParams(BaseModel):
    """Params"""

    email: str
    webinar_id: int
    application_id: int
    cancellation_token: str


def params(
    email: str, webinar_id: int, application_id: int, cancellation_token: str
) -> str:
    """Create params"""
    json_dump = json.dumps(
        SendSubmitterCancellationEmailParams(
            email=email,
            webinar_id=webinar_id,
            application_id=application_id,
            cancellation_token=cancellation_token,
        ).dict()
    )
    return json_dump


def send_submitter_cancellation_email(
    procedure_params: SendSubmitterCancellationEmailParams,
):
    """Send submitter confirmation email after application has been sent"""
    email_context = email_get_application_context(
        procedure_params.application_id
    )
    email_template = EmailTemplate(
        "email/EmailSubmitterCancellation.html",
        {
            **email_context,
            "cancellation_token": procedure_params.cancellation_token,
        },
    )

    webinar: Webinar = email_context["webinar"]
    webinar_date = _date(webinar.date, "j E Y")

    email_message = EmailMessage(
        email_template,
        f"Ważne informacje o szkoleniu w dniu {webinar_date}",
        procedure_params.email,
    )
    email_message.send()
