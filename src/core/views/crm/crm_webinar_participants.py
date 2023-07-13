from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar, WebinarParticipant
from core.services import CrmWebinarService


def crm_webinar_participants(request, pk: int):
    """Assets for given webinar"""
    template_name = "core/pages/crm/webinar/CrmWebinarParticipants.html"
    webinar = get_object_or_404(Webinar, pk=pk)
    webinar_service = CrmWebinarService(webinar)
    participants = (
        WebinarParticipant.manager.get_participants_from_sent_applications(
            webinar
        )
    )

    return TemplateResponse(
        request,
        template_name,
        {
            "webinar": webinar,
            "participants": participants,
            **webinar_service.get_context(),
        },
    )
