# flake8: noqa=E501

from django.core.paginator import Paginator
from django.template.response import TemplateResponse

from core.models import Webinar
from core.services import CrmWebinarService


def crm_archived_webinars(request):
    """CRM webinars archive"""
    template_name = "core/pages/crm/webinar/CrmArchivedWebinars.html"
    webinars = Webinar.manager.get_done_or_canceled_webinars().order_by("-date")

    paginator = Paginator(webinars, 50)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return TemplateResponse(
        request,
        template_name,
        {
            "webinars_ctxs": [
                CrmWebinarService(webinar).get_context() for webinar in page_obj
            ],
            "page_obj": page_obj,
        },
    )


def crm_archived_webinars_with_applications(request):
    """CRM webinars archive"""
    template_name = "core/pages/crm/webinar/CrmArchivedWebinarsWithApplications.html"
    webinars = Webinar.manager.get_canceled_webinars().order_by("-date")[:100]

    return TemplateResponse(
        request,
        template_name,
        {
            "webinars_ctxs": [
                CrmWebinarService(webinar).get_context() for webinar in webinars
            ]
        },
    )
