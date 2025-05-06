import json

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.notifications.email import (
    EmailMessage,
    EmailTemplate,
    sale_recording_email_get_application_context,
)


class SaleRecordingSendAccessEmailParams(BaseModel):
    """Params"""

    email: str
    application_id: int


def params(email: str, application_id: int) -> str:
    """Create params"""
    json_dump = json.dumps(
        SaleRecordingSendAccessEmailParams(
            email=email,
            application_id=application_id,
        ).dict()
    )
    return json_dump


def sale_recording_send_access_email(
    access_url: str,
    procedure_params: SaleRecordingSendAccessEmailParams,
):
    """Send participant opinion email"""
    template_name = "email/EmailSaleRecordingAccess.html"
    email_template = EmailTemplate(
        template_name,
        {
            "access_url": access_url,
            **sale_recording_email_get_application_context(
                procedure_params.application_id
            ),
        },
    )
    email_message = EmailMessage(
        email_template,
        "[WYKŁADOWCA.PL] Dostęp do nagrania ze szkolenia",
        procedure_params.email,
    )
    email_message.send()
