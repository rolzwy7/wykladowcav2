import json

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.notifications.email import (
    EmailMessage,
    EmailTemplate,
    email_get_application_context,
)


class SendParticipantCertificateEmailParams(BaseModel):
    """Params"""

    email: str
    application_id: int


def params(email: str, application_id: int) -> str:
    """Create params"""
    json_dump = json.dumps(
        SendParticipantCertificateEmailParams(
            email=email,
            application_id=application_id,
        ).dict()
    )
    return json_dump


def send_participant_certificate_email(
    certificate_url: str,
    procedure_params: SendParticipantCertificateEmailParams,
):
    """Send participant opinion email"""
    template_name = "email/EmailParticipantCertificate.html"
    email_template = EmailTemplate(
        template_name,
        {
            "certificate_url": certificate_url,
            **email_get_application_context(procedure_params.application_id),
        },
    )
    email_message = EmailMessage(
        email_template,
        "Certyfikat za udział w szkoleniu",
        procedure_params.email,
    )
    email_message.send()
