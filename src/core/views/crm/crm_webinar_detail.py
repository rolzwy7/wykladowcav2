from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar
from core.services import CrmWebinarService


def crm_webinar_detail_dashboard(
    request, pk: int
):  # TODO: Protect CRM endpoints
    webinar = get_object_or_404(Webinar, pk=pk)
    service = CrmWebinarService(webinar)
    return TemplateResponse(
        request,
        "core/pages/crm/webinar/CrmWebinarDetailDashboard.html",
        {**service.get_context()},
    )
