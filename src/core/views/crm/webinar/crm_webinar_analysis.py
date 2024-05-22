"""CRM webinar analysis"""

# pylint: disable=no-member

from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar, WebinarMetadata
from core.services import CrmWebinarService
from core.utils.analysis.pkd_analysis import analyse_pkd_for_applications


def crm_webinar_analysis(request, pk: int):
    """Webinar analysis"""
    template_name = "core/pages/crm/webinar/CrmWebinarAnalysis.html"
    webinar = get_object_or_404(Webinar, pk=pk)
    webinar_metadata = WebinarMetadata.objects.get(webinar=webinar)
    webinar_service = CrmWebinarService(webinar)
    sent_applications = webinar_service.get_sent_applications()

    return TemplateResponse(
        request,
        template_name,
        {
            "webinar": webinar,
            "webinar_metadata": webinar_metadata,
            "pkd_analysis": analyse_pkd_for_applications(sent_applications),
            **webinar_service.get_context(),
        },
    )
