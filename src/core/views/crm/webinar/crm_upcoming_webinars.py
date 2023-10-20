from django.db.models import Q
from django.template.response import TemplateResponse

from core.models import Webinar
from core.services import CrmWebinarService


def crm_upcoming_webinars(request):
    """CRM upcoming webinars"""
    template_name = "core/pages/crm/webinar/CrmUpcomingWebinars.html"

    webinars = Webinar.manager.get_init_or_confirmed_webinars()
    param_search = request.GET.get("search")
    if param_search:
        webinars = webinars.filter(
            Q(title_original__icontains=param_search)
            | Q(title__icontains=param_search)
            | Q(grouping_token__icontains=param_search)
            | Q(lecturer__fullname__icontains=param_search)
        )

    return TemplateResponse(
        request,
        template_name,
        {
            "upcoming_webinars_count": webinars.count(),
            "param_search": param_search or "",
            "webinars_ctxs": [
                CrmWebinarService(webinar).get_context() for webinar in webinars
            ],
        },
    )
