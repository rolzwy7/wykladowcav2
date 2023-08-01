from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar
from core.services import CrmWebinarService


def crm_webinar_certificates(request, pk: int):
    """Certificates for given webinar"""
    template_name = "core/pages/crm/webinar/CrmWebinarCertificates.html"
    webinar = get_object_or_404(Webinar, pk=pk)

    webinar_service = CrmWebinarService(webinar)

    return TemplateResponse(
        request,
        template_name,
        {
            "webinar": webinar,
            "certificates": webinar_service.get_certificates(),
            **webinar_service.get_context(),
        },
    )
