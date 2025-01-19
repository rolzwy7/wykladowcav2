"""webinar_aggregate_page"""

# flake8: noqa=E501

from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.models import Webinar, WebinarAggregate


def webinar_aggregate_page(request, slug: str):
    """webinar_aggregate_page"""
    template_name = "geeks/pages/webinarv3/WebinarAggregatePage.html"

    webinar_aggregate = get_object_or_404(WebinarAggregate, slug=slug)

    webinars = (
        Webinar.manager.get_active_webinars()
        .filter(grouping_token=webinar_aggregate.grouping_token)
        .order_by("date")
    )

    if webinars.exists():
        webinar = webinars.first()
    else:
        webinar = Webinar.manager.all().filter(
            grouping_token=webinar_aggregate.grouping_token
        )

    return TemplateResponse(
        request,
        template_name,
        {
            "webinar_aggregate": webinar_aggregate,
            "webinars": webinars,
            "webinar": webinar,
        },
    )
