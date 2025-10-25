"""crm_aggregates_page"""

# flake8: noqa=E501

from django.template.response import TemplateResponse

from core.models import Webinar, WebinarAggregate


def crm_aggregates_webinar_list_page(request):
    """crm_aggregates_webinar_list_page"""

    template_name = "core/pages/crm/CrmAggregatesList.html"

    q_grouping_token = request.GET.get("q_grouping_token")
    q_title = request.GET.get("q_title")
    q_lecturer = request.GET.get("q_lecturer")

    webinars = Webinar.manager.all()

    if q_grouping_token:
        if q_grouping_token == "pusty":
            webinars = webinars.filter(grouping_token="")
        else:
            webinars = webinars.filter(grouping_token__icontains=q_grouping_token)

    if q_title:
        webinars = webinars.filter(title=q_title)

    if q_lecturer:
        webinars = webinars.filter(lecturer__fullname=q_lecturer)

    return TemplateResponse(
        request,
        template_name,
        {
            "webinars": webinars,
            "q_grouping_token": q_grouping_token or "",
            "q_title": q_title or "",
            "q_lecturer": q_lecturer or "",
        },
    )


def crm_aggregates_page(request):
    """crm_aggregates_page"""
    template_name = "core/pages/crm/CrmAggregates.html"

    q_grouping_token = request.GET.get("q_grouping_token")
    only_without_active_webinars = request.GET.get("only_without_active_webinars")
    pod_szkolenie_zamkniete = request.GET.get("pod_szkolenie_zamkniete")

    if q_grouping_token:
        aggregates = WebinarAggregate.manager.filter(
            grouping_token__icontains=q_grouping_token
        )
    else:
        aggregates = WebinarAggregate.manager.all()

    if only_without_active_webinars:
        aggregates = aggregates.filter(has_active_webinars=False)

    if pod_szkolenie_zamkniete:
        aggregates = aggregates.filter(pod_szkolenie_zamkniete=True)

    return TemplateResponse(
        request,
        template_name,
        {
            "aggregates": aggregates.order_by("-created_at"),
            "only_without_active_webinars": only_without_active_webinars,
        },
    )
