# flake8: noqa:E501
from django.db.models import Q
from django.template.response import TemplateResponse
from django.utils import timezone

from core.models import Webinar, WebinarApplication
from core.models.enums import ApplicationStatus
from core.services import CrmWebinarService


def crm_upcoming_webinars(request):
    """CRM upcoming webinars"""

    webinars = Webinar.manager.get_init_or_confirmed_webinars()
    param_search = request.GET.get("search")
    if param_search:
        webinars = webinars.filter(
            Q(title_original__icontains=param_search)
            | Q(title__icontains=param_search)
            | Q(grouping_token__icontains=param_search)
            | Q(lecturer__fullname__icontains=param_search)
        )

    sent_today_paid_applications = WebinarApplication.manager.filter(
        status=ApplicationStatus.SENT, created_at__date=timezone.now().date()
    )

    return TemplateResponse(
        request,
        "core/pages/crm/webinar/CrmUpcomingWebinars.html",
        {
            "upcoming_webinars_count": webinars.count(),
            "sent_today_paid_applications": sent_today_paid_applications,
            "sent_today_paid_applications_count": sent_today_paid_applications.count(),
            "param_search": param_search or "",
            # "webinars_ctxs": [
            #     CrmWebinarService(webinar).get_context() for webinar in webinars
            # ],
            "webinars_ctxs_upcoming_webinar_row": [
                CrmWebinarService(webinar).get_upcoming_webinar_row_context()
                for webinar in webinars
            ],
        },
    )
