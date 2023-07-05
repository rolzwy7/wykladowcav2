import json

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.notifications.email import EmailMessage, EmailTemplate
from core.models import Lecturer, Webinar


class SendParticipantCertificateEmailParams(BaseModel):
    """Params"""

    email: str
    webinar_title: str
    lecturer: str


def params(email: str, webinar: Webinar) -> str:
    """Create params"""
    lecturer: Lecturer = webinar.lecturer
    json_dump = json.dumps(
        SendParticipantCertificateEmailParams(
            email=email,
            webinar_title=webinar.title_original,
            lecturer=lecturer.fullname,
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
            "webinar_title": procedure_params.webinar_title,
            "lecturer": procedure_params.lecturer,
        },
    )
    email_message = EmailMessage(
        email_template,
        "Certyfikat za udział w szkoleniu",
        procedure_params.email,
    )
    email_message.send()
