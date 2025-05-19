"""webinar_aggregate lib"""

# flake8: noqa=E501

from random import randint

from django.shortcuts import redirect
from django.urls import reverse

from core.models import Webinar, WebinarAggregate


def resolve_aggregate_redirect(aggregate: WebinarAggregate):
    """resolve_aggregate_redirect"""

    # If first aggregate has absolute redirect
    if aggregate.absolute_redirect:
        return redirect(aggregate.absolute_redirect)

    aggregate_ids = []
    temp_aggregate = aggregate
    ret_redirect = None
    while temp_aggregate.parent:
        # Check for cyclic reference
        if temp_aggregate.slug in aggregate_ids:
            raise ValueError("Aggregate cyclic reference detected")
        else:
            aggregate_ids.append(temp_aggregate.slug)
        temp_aggregate = temp_aggregate.parent

        # If parent has absolute redirect
        if temp_aggregate.absolute_redirect:
            return redirect(temp_aggregate.absolute_redirect)

        ret_redirect = redirect(
            reverse("core:webinar_aggregate_page", kwargs={"slug": temp_aggregate.slug})
        )

    return ret_redirect


def connect_webinar_to_aggregate(webinar: Webinar):
    """Connect aggregate to webinar"""

    try:
        # Check if aggregate with given grouping token already exists
        aggregate: WebinarAggregate = WebinarAggregate.manager.get(
            grouping_token=webinar.grouping_token
        )
    except WebinarAggregate.DoesNotExist:  # pylint: disable=no-member
        # Create new aggregate
        webinar_core_slug = "-".join(webinar.slug.split("-")[:-1])
        slug_conflict = WebinarAggregate.manager.filter(slug=webinar_core_slug).exists()
        new_aggregate: WebinarAggregate = WebinarAggregate(
            title=webinar.title,
            grouping_token=webinar.grouping_token,
            slug_conflict=slug_conflict,
            slug=(
                f"CONFLICT-{randint(1_000, 99_999)}-{slug_conflict}"
                if slug_conflict
                else webinar_core_slug
            ),
        )
        new_aggregate.save()
        # Add webinar to newly created aggregate
        new_aggregate.webinars.add(webinar)  # pylint: disable=no-member
        for cat in webinar.categories.all():
            new_aggregate.categories.add(cat)  # pylint: disable=no-member
    else:
        # Add webinar to aggregate
        aggregate.webinars.add(webinar)
        for cat in webinar.categories.all():
            aggregate.categories.add(cat)
