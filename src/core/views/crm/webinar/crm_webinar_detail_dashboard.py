from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar
from core.services import CrmWebinarService


def crm_webinar_detail_dashboard(request, pk: int):
    """CRM dashboard for webinar"""
    webinar = get_object_or_404(Webinar, pk=pk)
    service = CrmWebinarService(webinar)
    sent_applications_metadata = service.get_sent_applications_metadata()
    return TemplateResponse(
        request,
        "core/pages/crm/webinar/CrmWebinarDetailDashboard.html",
        {
            "cancellations": service.get_applications_cancellations(),
            "move_registers": service.get_move_registers(),
            "sent_applications_metadata": sent_applications_metadata,
            **service.get_context(),
        },
    )
