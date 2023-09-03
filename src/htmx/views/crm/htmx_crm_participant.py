from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.cache import cache_page

from core.consts import POST
from core.models import WebinarParticipant, WebinarParticipantMetadata
from core.services import MxService


def htmx_crm_participant_toggle_phoned(request: HttpRequest, pk: int):
    """Toggle CRM participant phoned"""
    template_path = "htmx/participant_toggle_phoned.html"
    participant = get_object_or_404(WebinarParticipant, pk=pk)
    metadata = get_object_or_404(
        WebinarParticipantMetadata, participant=participant
    )

    if request.method == POST:
        metadata.phoned = not metadata.phoned
        metadata.save()

    return TemplateResponse(
        request,
        template_path,
        {"participant": participant, "phoned": metadata.phoned},
    )


@cache_page(15 * 60)
def htmx_crm_participant_indicators(request: HttpRequest, pk: int):
    """Toggle CRM participant phoned"""
    template_path = "htmx/participant_indicators.html"
    participant = get_object_or_404(WebinarParticipant, pk=pk)
    metadata = get_object_or_404(
        WebinarParticipantMetadata, participant=participant
    )
    mx_service = MxService()

    status = participant.application.webinar.status
    clickmeeting_invitation_send = metadata.clickmeeting_invitation_send

    # Check MX
    is_mx_valid = mx_service.has_email_mx_record(participant.email)
    metadata.is_mx_valid = "VALID" if is_mx_valid else "INVALID"
    metadata.save()

    # Check if participant was registered before
    same_participants = WebinarParticipant.manager.filter(
        email=participant.email
    ).count()
    new_participant = same_participants == 1

    return TemplateResponse(
        request,
        template_path,
        {
            "participant": participant,
            "is_mx_valid": metadata.is_mx_valid,
            "new_participant": new_participant,
            "clickmeeting_invitation_send": clickmeeting_invitation_send,
            "webinar_status": status,
        },
    )
