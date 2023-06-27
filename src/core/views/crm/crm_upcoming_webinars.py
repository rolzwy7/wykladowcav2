from django.template.response import TemplateResponse

from core.models import Webinar


def crm_upcoming_webinars(request):
    context = {"webinars": Webinar.manager.init_or_confirmed()}
    return TemplateResponse(
        request, "core/pages/crm/CrmUpcomingWebinars.html", context
    )
