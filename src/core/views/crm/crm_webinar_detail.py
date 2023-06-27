from django.template.response import TemplateResponse

from core.models import Webinar


def crm_webinar_detail_dashboard(request, pk: int):
    context = {}
    return TemplateResponse(
        request,
        "core/pages/crm/webinar/CrmUWebinarDetailDashboard.html",
        context,
    )
