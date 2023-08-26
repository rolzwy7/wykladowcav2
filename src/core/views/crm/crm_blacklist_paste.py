from django.template.response import TemplateResponse

from core.models import Webinar


def crm_blacklist_paste(request):  # TODO
    """CRM paste blacklist"""
    template_name = "core/pages/crm/CrmBlacklistPaste.html"
    webinars = Webinar.manager.done_or_canceled()

    return TemplateResponse(
        request,
        template_name,
        {},
    )
