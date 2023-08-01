from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Eventlog, Webinar
from core.services import CrmWebinarService


def crm_webinar_eventlogs(request, pk: int):
    """Eventlogs for given webinar"""
    template_name = "core/pages/crm/webinar/CrmWebinarEventlogs.html"
    webinar = get_object_or_404(Webinar, pk=pk)
    webinar_eventlogs = Eventlog.manager.filter(webinar=webinar)
    service = CrmWebinarService(webinar)
    return TemplateResponse(
        request,
        template_name,
        {
            "webinar": webinar,
            "webinar_eventlogs": webinar_eventlogs,
            **service.get_context(),
        },
    )
