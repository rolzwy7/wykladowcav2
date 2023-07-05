from django.template.response import TemplateResponse

from core.models import Webinar


def crm_archived_webinars(request):
    template_name = "core/pages/crm/webinar/CrmArchivedWebinars.html"
    webinar = Webinar.manager.done_or_canceled()
    return TemplateResponse(
        request,
        template_name,
        {"webinars": webinar},
    )
