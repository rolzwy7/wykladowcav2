# flake8: noqa=E501

import json

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.notifications.email import (
    EmailMessage,
    EmailTemplate,
    sale_recording_email_get_application_context,
)


class SendSaleRecordingOrderEmailParams(BaseModel):
    """Params"""

    email: str
    application_id: int


def params(email: str, application_id: int) -> str:
    """Create params"""
    json_dump = json.dumps(
        SendSaleRecordingOrderEmailParams(
            email=email, application_id=application_id
        ).dict()
    )
    return json_dump


def send_sale_recording_order_email(
    procedure_params: SendSaleRecordingOrderEmailParams,
):
    """Send sale recording order email"""
    email_template = EmailTemplate(
        "email/EmailSaleRecordingOrder.html",
        sale_recording_email_get_application_context(procedure_params.application_id),
    )
    email_message = EmailMessage(
        email_template,
        "[WYKŁADOWCA.PL] Otrzymaliśmy twoje zamówienie!",
        procedure_params.email,
    )
    email_message.send()
