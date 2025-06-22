"""CRM Redirect"""

# flake8: noqa=E501

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from core.models import WebinarAggregate


def crm_redirect(request, name: str, param: str):
    """crm_redirect"""

    if name == "aggregate_site":
        aggregate: WebinarAggregate = WebinarAggregate.manager.get(grouping_token=param)
        return redirect(
            reverse("core:webinar_aggregate_page", kwargs={"slug": aggregate.slug})
        )

    if name == "aggregate_cms":
        aggregate: WebinarAggregate = WebinarAggregate.manager.get(grouping_token=param)
        return redirect(
            reverse(
                "admin:core_webinaraggregate_change",
                kwargs={"object_id": aggregate.grouping_token},
            )
        )

    return HttpResponse("invalid `name` or `param` values")
