from django.conf import settings
from django.urls import reverse
from django.utils.timezone import now

from core.models import (
    Webinar,
    WebinarApplication,
    WebinarCertificate,
    WebinarParticipant,
)


def create_participant_certificate(participant_id: int) -> str:
    """Create certificate for participant and return URL"""

    participant = WebinarParticipant.manager.get(id=participant_id)
    application: WebinarApplication = participant.application
    webinar: Webinar = application.webinar

    certificate = WebinarCertificate(
        first_name=participant.first_name,
        last_name=participant.last_name,
        title=webinar.title_original,
        issue_date=now(),
        hours=webinar.get_duration_display(),  # type: ignore
        participant=participant,
    )

    certificate.save()

    return settings.BASE_URL + reverse(
        "core:certificate_pdf_page",
        kwargs={"uuid": certificate.uuid},
    )
