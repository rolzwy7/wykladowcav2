"""send_participant_opinion_email procedure"""

# flake8: noqa=E501

import json
from random import choice

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.notifications.email import (
    EmailMessage,
    EmailTemplate,
    email_get_application_context,
)


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
    email_context = email_get_application_context(procedure_params.application_id)
    email_template = EmailTemplate(
        template_name,
        {**email_context},
    )
    lecturer_fullname = email_context["lecturer"].fullname
    email_message = EmailMessage(
        email_template,
        choice(
            [
                f"Prośba o przesłanie opinii o wykładowcy - {lecturer_fullname}",
                f"Przekaż nam swoją opinię o wykładowcy - {lecturer_fullname}",
                f"Prosimy o przesłanie opinii o wykładowcy - {lecturer_fullname}",
            ]
        ),
        procedure_params.email,
    )
    email_message.send()
