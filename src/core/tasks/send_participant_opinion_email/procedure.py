import json

from django.conf import settings
from django.template.defaultfilters import date as _date
from django.urls import reverse
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.notifications.email import (
    EmailMessage,
    EmailTemplate,
    email_get_application_context,
)
from core.models import Lecturer, Webinar


class SendParticipantOpinionEmailParams(BaseModel):
    """Params"""

    email: str
    application_id: int


def params(email: str, application_id: int) -> str:
    """Create params"""
    json_dump = json.dumps(
        SendParticipantOpinionEmailParams(
            email=email,
            application_id=application_id,
        ).dict()
    )
    return json_dump


def send_participant_opinion_email(
    procedure_params: SendParticipantOpinionEmailParams,
):
    """Send participant opinion email"""
    template_name = "email/EmailParticipantOpinion.html"
    email_template = EmailTemplate(
        template_name,
        {**email_get_application_context(procedure_params.application_id)},
    )
    email_message = EmailMessage(
        email_template,
        "Prośba o przesłanie opinii o wykładowcy",
        procedure_params.email,
    )
    email_message.send()
