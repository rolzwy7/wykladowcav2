from django.template.response import TemplateResponse

from core.models import Webinar
from core.services import CrmWebinarService


def crm_upcoming_webinars(request):
    """CRM upcoming webinars"""
    template_name = "core/pages/crm/webinar/CrmUpcomingWebinars.html"
    webinars = Webinar.manager.init_or_confirmed()

    return TemplateResponse(
        request,
        template_name,
        {
            "webinars_ctxs": [
                CrmWebinarService(webinar).get_context() for webinar in webinars
            ]
        },
    )
