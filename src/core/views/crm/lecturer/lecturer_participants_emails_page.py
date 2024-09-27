"""lecturer_participants_emails_page"""

# flake8: noqa=E501

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from core.models.enums import WebinarStatus
from core.models.lecturer_model import Lecturer
from core.models.webinar_participant_model import WebinarParticipant


def lecturer_participants_emails_page(request, pk: int, participants_type: str):
    """lecturer_participants_emails_page"""
    lecturer = get_object_or_404(Lecturer, pk=pk)

    include_all_webinars = request.GET.get("include_all_webinars")

    if participants_type == "paid-participants":

        if include_all_webinars:
            paid_pairticipants = WebinarParticipant.manager.filter(
                application__webinar__lecturer=lecturer
            )
        else:
            paid_pairticipants = WebinarParticipant.manager.filter(
                Q(application__webinar__lecturer=lecturer)
                & Q(application__webinar__status=WebinarStatus.DONE)
            )

        emails: list[str] = [_.email for _ in paid_pairticipants]
    elif participants_type == "free-participants":
        emails: list[str] = []

    return HttpResponse(
        "\n".join(set(emails)),
        content_type="text/plain; charset=utf8",
    )
