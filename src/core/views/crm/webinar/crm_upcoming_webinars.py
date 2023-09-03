from django.template.response import TemplateResponse

from core.models import Webinar
from core.services import CrmWebinarService


def crm_upcoming_webinars(request):
    """CRM upcoming webinars"""
    template_name = "core/pages/crm/webinar/CrmUpcomingWebinars.html"
    webinars = Webinar.manager.get_init_or_confirmed_webinars()

    return TemplateResponse(
        request,
        template_name,
        {
            "upcoming_webinars_count": webinars.count(),
            "webinars_ctxs": [
                CrmWebinarService(webinar).get_context() for webinar in webinars
            ],
        },
    )
