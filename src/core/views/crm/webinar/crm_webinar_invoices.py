from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar
from core.services import CrmWebinarService


def crm_webinar_invoices(request, pk: int):
    """Invoices for given webinar"""
    template_name = "core/pages/crm/webinar/CrmWebinarInvoices.html"
    webinar = get_object_or_404(Webinar, pk=pk)
    service = CrmWebinarService(webinar)

    sent_applications_metadata = service.get_sent_applications_metadata()
    return TemplateResponse(
        request,
        template_name,
        {
            "webinar": webinar,
            "sent_applications_metadata": sent_applications_metadata,
            **service.get_context(),
        },
    )
