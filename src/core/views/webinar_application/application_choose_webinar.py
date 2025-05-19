"""Application form type"""

# flake8: noqa:E501
# pylint: disable=line-too-long

from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import WebinarAggregate


def application_choose_webinar(request, slug: str):
    """application_choose_webinar"""
    template_name = "geeks/pages/application/ApplicationChooseWebinarPage.html"

    webinar_aggregate = get_object_or_404(WebinarAggregate, slug=slug)

    return TemplateResponse(
        request,
        template_name,
        {
            "webinar_aggregate": webinar_aggregate,
            "webinars": webinar_aggregate.webinars.all(),
        },
    )
