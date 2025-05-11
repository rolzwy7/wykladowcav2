# flake8: noqa:E501
from django.conf import settings
from django.db.models import Q
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.timezone import now

from core.models import CrmNote, Webinar, WebinarApplication
from core.models.enums import ApplicationStatus
from core.services import CrmWebinarService


def crm_upcoming_webinars(request):
    """CRM upcoming webinars"""

    webinars = Webinar.manager.get_init_or_confirmed_or_draft_webinars()

    param_any = False

    # Show only drafts
    param_show_only_drafts = request.GET.get("show_only_drafts")
    if param_show_only_drafts:
        param_any = True
        webinars = Webinar.manager.get_draft_webinars()
    else:
        webinars = Webinar.manager.get_init_or_confirmed_or_draft_webinars()

    # Show counters
    param_show_counters = request.GET.get("show_counters")
    if param_show_counters:
        param_any = True

    # Hide old webinars
    param_hide_old = request.GET.get("hide_old")
    if param_hide_old:
        webinars = webinars.filter(date__gt=now())
        param_any = True

    # Hide fake param
    param_hide_fake = request.GET.get("hide_fake")
    if param_hide_fake:
        webinars = webinars.filter(is_fake=False)
        param_any = True

    # Search param
    param_search = request.GET.get("search")
    if param_search:
        webinars = webinars.filter(
            Q(title_original__icontains=param_search)
            | Q(title__icontains=param_search)
            | Q(grouping_token__icontains=param_search)
            | Q(lecturer__fullname__icontains=param_search)
        )
        param_any = True

    sent_today_paid_applications = WebinarApplication.manager.filter(
        status=ApplicationStatus.SENT, created_at__date=timezone.now().date()
    )

    return TemplateResponse(
        request,
        "core/pages/crm/webinar/CrmUpcomingWebinars.html",
        {
            "crm_notes": CrmNote.manager.get_notes(),
            "upcoming_webinars_count": webinars.count(),
            "sent_today_paid_applications": sent_today_paid_applications,
            "sent_today_paid_applications_count": sent_today_paid_applications.count(),
            "mailing_processes_num": settings.MAILING_NUM_OF_PROCESSES,
            "param_any": param_any,
            "param_hide_old": param_hide_old,
            "param_search": param_search or "",
            "param_hide_fake": param_hide_fake,
            "param_show_counters": param_show_counters,
            "param_show_only_drafts": param_show_only_drafts,
            # "webinars_ctxs": [
            #     CrmWebinarService(webinar).get_context() for webinar in webinars
            # ],
            "webinars_ctxs_upcoming_webinar_row": [
                CrmWebinarService(webinar).get_upcoming_webinar_row_context()
                for webinar in webinars
            ],
        },
    )
