import json

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.notifications.email import EmailMessage, EmailTemplate
from core.models import Webinar


class SendParticipantPreparationEmailParams(BaseModel):
    """Params"""

    webinar_id: int
    email: str


def params(email: str, webinar: Webinar) -> str:
    """Create params"""
    webinar_id: int = webinar.id  # type: ignore
    json_dump = json.dumps(
        SendParticipantPreparationEmailParams(
            webinar_id=webinar_id, email=email
        ).dict()
    )
    return json_dump


def send_participant_preparation_email(
    procedure_params: SendParticipantPreparationEmailParams,
):
    """Send participant confirmation email after application has been sent"""
    email_template = EmailTemplate("email/EmailParticipantPreparation.html", {})
    email_message = EmailMessage(
        email_template,
        "Termin szkolenia został potwierdzony",
        procedure_params.email,
    )
    email_message.send()

    # TODO: eventlog_participant_confirmation_email(
    #     procedure_params.webinar_id, procedure_params.email
    # )
