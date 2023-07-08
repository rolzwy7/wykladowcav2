from django.template.response import TemplateResponse

from core.models import Webinar


def crm_upcoming_webinars(request):
    """CRM upcoming webinars"""
    template_name = "core/pages/crm/webinar/CrmUpcomingWebinars.html"
    webinar = Webinar.manager.init_or_confirmed()
    return TemplateResponse(
        request,
        template_name,
        {"webinars": webinar},
    )
