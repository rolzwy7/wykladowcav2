"""crm_webinar_free_participants"""

# flake8: noqa=E501

from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar
from core.services import CrmWebinarService


def crm_webinar_free_participants(request, pk: int):
    """crm_webinar_free_participants"""
    template_name = "core/pages/crm/webinar/CrmWebinarFreeParticipants.html"
    webinar = get_object_or_404(Webinar, pk=pk)
    service = CrmWebinarService(webinar)

    return TemplateResponse(
        request,
        template_name,
        {
            "webinar": webinar,
            **service.get_context(),
        },
    )
