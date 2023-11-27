from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.timezone import now

from core.models import Webinar
from core.services import CrmWebinarService


def crm_webinar_recordings(request, pk: int):
    """Recordings for given webinar"""
    template_name = "core/pages/crm/webinar/CrmWebinarRecordings.html"
    webinar = get_object_or_404(Webinar, pk=pk)

    webinar_service = CrmWebinarService(webinar)

    return TemplateResponse(
        request,
        template_name,
        {
            "webinar": webinar,
            "recordings": webinar_service.get_recordings(),
            "all_tokens": webinar_service.get_all_recording_tokens(),
            "now": now(),
            **webinar_service.get_context(),
        },
    )
