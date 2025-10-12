"""webinar_aggregate_page"""

# flake8: noqa=E501

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.libs.webinar_aggregate import resolve_aggregate_redirect
from core.models import Webinar, WebinarAggregate


def webinar_aggregate_page(request, slug: str):
    """webinar_aggregate_page"""
    template_name = "geeks/pages/webinar_aggregate/WebinarAggregatePage.html"

    show_queue_form = request.GET.get("show_queue_form")

    # Get webinar aggregate
    aggregate = get_object_or_404(WebinarAggregate, slug=slug)

    agg_redirect = resolve_aggregate_redirect(aggregate)
    if agg_redirect:
        return agg_redirect

    # Get all webinars from aggregate
    aggregate_all_webinars = aggregate.webinars.all().order_by("date")

    # If aggregate doesn't have any webinar return 404
    if all([not aggregate_all_webinars, not aggregate.pod_szkolenie_zamkniete]):
        return Http404()

    # Get first webinar as reference webinar
    first_webinar = aggregate_all_webinars.first()

    # Get all active webinars on webiste
    active_webinars = Webinar.manager.get_active_webinars()

    # Get active and inactive webinars for this aggregate
    aggregate_active_webinars: list[Webinar] = []
    aggregate_inactive_webinars: list[Webinar] = []

    for _ in aggregate_all_webinars:
        if active_webinars.filter(id=_.id).exists():
            aggregate_active_webinars.append(_)
        else:
            aggregate_inactive_webinars.append(_)

    any_active_webinar = bool(aggregate_active_webinars)

    # If any webinar is anonymized -> whole aggragate is anonymized
    anonymized = any([_.is_lecturer_anonymized for _ in aggregate_all_webinars])

    # Get lecturer
    if anonymized:
        lecturer = None
    else:
        lecturer = aggregate.lecturer  # type: ignore

    # Categories (only names)
    set_category_names = set()
    for category in aggregate.categories.all():
        set_category_names.add(category.name)

    return TemplateResponse(
        request,
        template_name,
        {
            "aggregate": aggregate,
            "first_webinar": first_webinar,
            "anonymized": anonymized,
            "any_active_webinar": any_active_webinar,
            "lecturer": lecturer,
            "aggregate_active_webinars": aggregate_active_webinars,
            "aggregate_inactive_webinars": aggregate_inactive_webinars,
            "set_category_names": set_category_names,
            "show_queue_form": show_queue_form,
        },
    )
