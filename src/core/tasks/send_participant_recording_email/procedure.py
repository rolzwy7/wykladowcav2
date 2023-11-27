# flake8: noqa:E501
# pylint: disable=line-too-long
import json

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.notifications.email import (
    EmailMessage,
    EmailTemplate,
    email_get_application_context,
)


class SendParticipantRecordingEmailParams(BaseModel):
    """Params"""

    email: str
    webinar_id: int
    application_id: int
    access_url: str
    expiration_date_human: str


def params(
    email: str,
    webinar_id: int,
    application_id: int,
    access_url: str,
    expiration_date_human: str,
) -> str:
    """Create params"""
    json_dump = json.dumps(
        SendParticipantRecordingEmailParams(
            email=email,
            webinar_id=webinar_id,
            application_id=application_id,
            access_url=access_url,
            expiration_date_human=expiration_date_human,
        ).dict()
    )
    return json_dump


def send_participant_recording_email(
    procedure_params: SendParticipantRecordingEmailParams,
):
    """Send participant confirmation email after application has been sent"""

    email_template = EmailTemplate(
        "email/EmailParticipantRecording.html",
        {
            **email_get_application_context(procedure_params.application_id),
            "access_url": procedure_params.access_url,
            "expiration_date_human": procedure_params.expiration_date_human,
        },
    )
    email_message = EmailMessage(
        email_template,
        "Dostęp do nagrania ze szkolenia",
        procedure_params.email,
    )
    email_message.send()
