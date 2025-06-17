"""webinar_aggregate lib"""

# flake8: noqa=E501

from hashlib import sha256
from random import randint

from django.shortcuts import redirect
from django.urls import reverse
from django.utils.timezone import datetime, now, timedelta

from core.models import Webinar, WebinarAggregate, WebinarCategory


def get_or_create_aggregate(webinar: Webinar):
    """get_or_create_aggregate"""

    try:
        # Check if aggregate with given grouping token already exists
        aggregate: WebinarAggregate = WebinarAggregate.manager.get(
            grouping_token=webinar.grouping_token
        )

        # If it exists fill blank fields
        save_needed = False
        if not aggregate.title:
            aggregate.title = webinar.title
            save_needed = True

        if not aggregate.program:
            aggregate.program = webinar.program
            save_needed = True

        if not aggregate.program_assets:
            aggregate.program_assets = webinar.program_assets
            save_needed = True

        if not aggregate.lecturer:
            aggregate.lecturer = webinar.lecturer
            save_needed = True

        if save_needed:
            aggregate.save()

        return aggregate
    except WebinarAggregate.DoesNotExist:  # pylint: disable=no-member
        # Create new aggregate
        webinar_core_slug = "-".join(webinar.slug.split("-")[:-1])
        slug_conflict = WebinarAggregate.manager.filter(slug=webinar_core_slug).exists()
        new_aggregate: WebinarAggregate = WebinarAggregate(
            hidden=False,
            title=webinar.title,
            grouping_token=webinar.grouping_token,
            slug_conflict=slug_conflict,
            program=webinar.program,
            program_assets=webinar.program_assets,
            lecturer=webinar.lecturer,
            slug=(
                f"CONFLICT-{randint(1_000, 99_999)}-{slug_conflict}"
                if slug_conflict
                else webinar_core_slug
            ),
        )
        new_aggregate.save()
        return new_aggregate


def aggregate_clear_webinars(aggregate: WebinarAggregate):
    """aggregate_clear_webinars"""
    aggregate.webinars.clear()


def aggregate_add_webinar(aggregate: WebinarAggregate, webinar: Webinar):
    """aggregate_add_webinar"""
    aggregate.webinars.add(webinar)


def relink_webinars_for_aggregate(aggregate: WebinarAggregate):
    """relink_webinars_for_aggregate"""

    # Get all webinars with aggregate's grouping token
    webinars_for_token = Webinar.manager.filter(grouping_token=aggregate.grouping_token)

    # Clear webinars for aggregate
    aggregate_clear_webinars(aggregate)

    # Re-link webinars with aggregate
    for webinar in webinars_for_token:
        aggregate_add_webinar(aggregate, webinar)


def aggregate_clear_categories(aggregate: WebinarAggregate):
    """aggregate_clear_categories"""
    aggregate.categories.clear()


def aggregate_add_category(aggregate: WebinarAggregate, category: WebinarCategory):
    """aggregate_add_category"""
    aggregate.categories.add(category)


def aggregate_refresh_categories(aggregate: WebinarAggregate):
    """aggregate_refresh_categories"""
    # Clear categories
    aggregate.categories.clear()
    # Re-add categories from webinars
    for _webinar in aggregate.webinars.all():
        webinar: Webinar = _webinar
        for _category in webinar.categories.all():
            category: WebinarCategory = _category
            aggregate.categories.add(category)


def aggregate_update_closest_webinar_dt(aggregate: WebinarAggregate):
    """aggregate_update_closest_webinar_dt"""

    base_dt = now() + timedelta(days=365 * 10)
    active_webinars = Webinar.manager.get_active_webinars()
    active_webinars_ids = {_.id: True for _ in active_webinars}  # type: ignore

    for _webinar in aggregate.webinars.all():
        webinar: Webinar = _webinar
        webinar_id: int = webinar.id  # type: ignore

        if not active_webinars_ids.get(webinar_id):
            continue

        if webinar.date < base_dt:
            base_dt = webinar.date

    aggregate.closest_webinar_dt = base_dt
    aggregate.save()


def aggregate_update_has_active_webinars(aggregate: WebinarAggregate):
    """aggregate_update_has_active_webinars"""

    active_webinars = Webinar.manager.get_active_webinars()
    active_webinars_ids = {_.id: True for _ in active_webinars}  # type: ignore

    has_active_webinars = False
    for _webinar in aggregate.webinars.all():
        webinar: Webinar = _webinar
        webinar_id: int = webinar.id  # type: ignore
        if active_webinars_ids.get(webinar_id):
            has_active_webinars = True
            break

    aggregate.has_active_webinars = has_active_webinars
    aggregate.save()


def aggregate_update_conflicts(aggregate: WebinarAggregate):
    """aggregate_update_conflicts"""

    active_webinars = Webinar.manager.get_init_or_confirmed_webinars()
    active_webinars_ids = {_.id: True for _ in active_webinars}  # type: ignore

    titles = set()
    lecturers = set()
    program_hashes = set()
    program_assets_hashes = set()

    for _webinar in aggregate.webinars.all():
        webinar: Webinar = _webinar
        webinar_id: int = webinar.id  # type: ignore
        webinar_program: str = webinar.program
        webinar_program_assets: str = webinar.program_assets

        # Only active webinars
        if not active_webinars_ids.get(webinar_id):
            continue

        if not aggregate.lecturer:
            aggregate.lecturer = webinar.lecturer

        titles.add(webinar.title)
        lecturers.add(webinar.lecturer.id)
        program_hashes.add(sha256(webinar_program.encode()).hexdigest())
        program_assets_hashes.add(sha256(webinar_program_assets.encode()).hexdigest())

    # Title conflict
    aggregate.title_conflict = len(titles) != 1
    aggregate.program_conflict = len(program_hashes) != 1
    aggregate.program_assets_conflict = len(program_assets_hashes) != 1
    aggregate.lecturer_conflict = len(lecturers) != 1

    aggregate.save()


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
