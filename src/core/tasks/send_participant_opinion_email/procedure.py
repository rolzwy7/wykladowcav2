import json

from django.conf import settings
from django.template.defaultfilters import date as _date
from django.urls import reverse
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.notifications.email import EmailMessage, EmailTemplate
from core.models import Lecturer, Webinar


class SendParticipantOpinionEmailParams(BaseModel):
    """Params"""

    email: str
    webinar_title: str
    webinar_date: str
    lecturer_opinion_url: str


def params(email: str, webinar: Webinar) -> str:
    """Create params"""
    lecturer: Lecturer = webinar.lecturer
    lecturer_opinion_url = settings.BASE_URL + reverse(
        "core:lecturer_opinion_form_page",
        kwargs={"slug": lecturer.slug},
    )

    json_dump = json.dumps(
        SendParticipantOpinionEmailParams(
            email=email,
            webinar_title=webinar.title_original,
            webinar_date=_date(webinar.date, "j E Y"),
            lecturer_opinion_url=lecturer_opinion_url,
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
        {
            "webinar_title": procedure_params.webinar_title,
            "webinar_date": procedure_params.webinar_date,
            "lecturer_opinion_url": procedure_params.lecturer_opinion_url,
        },
    )
    email_message = EmailMessage(
        email_template,
        "Prośba o przesłanie opinii o wykładowcy",
        procedure_params.email,
    )
    email_message.send()
