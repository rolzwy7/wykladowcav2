from django.template.response import TemplateResponse

from core.models import Eventlog


def crm_eventlogs(request):
    """All eventlogs"""
    template_name = "core/pages/crm/CrmEventlogs.html"
    return TemplateResponse(
        request,
        template_name,
        {
            "eventlogs_today": Eventlog.manager.todays_eventlogs(),
            "eventlogs_month": Eventlog.manager.this_month_eventlogs(),
        },
    )
