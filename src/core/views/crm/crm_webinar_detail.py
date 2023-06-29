from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar


def crm_webinar_detail_dashboard(request, pk: int):
    webinar = get_object_or_404(Webinar, pk=pk)
    return TemplateResponse(
        request,
        "core/pages/crm/webinar/CrmWebinarDetailDashboard.html",
        {"webinar": webinar},
    )
