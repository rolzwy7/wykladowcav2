# flake8: noqa=E501

from django.forms import CheckboxInput, ModelForm, Select, TextInput
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.timezone import now

from core.consts.requests_consts import POST
from core.models import (
    ConferenceCycle,
    ConferenceEdition,
    ConferenceFreeParticipant,
    ConferenceSchedule,
    Webinar,
)
from core.models.enums import LeadSource
from core.services.lead_service import LeadService
from core.tasks_dispatch import after_free_conference_participant_singup


class ConferenceFreeParticipantModelForm(ModelForm):
    """ConferenceFreeParticipantModelForm"""

    class Meta:
        model = ConferenceFreeParticipant
        fields = [
            "first_name",
            "last_name",
            "voivodeship",
            "phone",
            "email",
            "know_from",
            "using_closed_webinars",
            "consent",
        ]

        widgets = {
            "first_name": TextInput(attrs={"class": "form-control"}),
            "last_name": TextInput(attrs={"class": "form-control"}),
            "voivodeship": Select(attrs={"class": "form-control"}),
            "phone": TextInput(attrs={"class": "form-control"}),
            "email": TextInput(attrs={"class": "form-control"}),
            "know_from": Select(attrs={"class": "form-control"}),
            "using_closed_webinars": Select(attrs={"class": "form-control"}),
            "consent": CheckboxInput(attrs={"class": "form-check-input"}),
        }


def conference_edition_page(request: HttpRequest, slug_cycle: str, slug_edition: str):
    """Conference cycle page"""
    template_name = "geeks/pages/conference/ConferenceEditionPage.html"
    cycle = get_object_or_404(ConferenceCycle, slug=slug_cycle)
    edition = get_object_or_404(ConferenceEdition, slug=slug_edition)
    schedule = ConferenceSchedule.manager.filter(edition=edition).order_by("hour_from")

    has_started = now() > edition.date_from

    # Determine status
    if now() < edition.date_from:
        status = "INIT"
    elif now() >= edition.date_from and now() <= edition.date_to:
        status = "IN_PROGRESS"
    else:
        status = "DONE"

    # Return error if schedule not set
    if not schedule.exists():
        return HttpResponse("Harmonogram nie został dodany")

    # Prepare data
    first_schedule: ConferenceSchedule = schedule.first()  # type: ignore
    lecturers = [sch.lecturer for sch in schedule if sch.lecturer]

    # Handle form submission
    if request.method == POST:
        form = ConferenceFreeParticipantModelForm(request.POST)
        if form.is_valid():
            # Save free participant with form
            participant: ConferenceFreeParticipant = form.save(commit=False)
            participant.edition = edition
            participant.save()
            # Save lead
            lead = LeadService.get_or_create_lead(
                participant.email,
                LeadSource.CONFERENCE_FREE,
                request=request,
                categories=[
                    *[_ for _ in cycle.categories.all()],
                    *[_ for _ in edition.categories.all()],
                ],
            )
            LeadService.apply_basic_data(
                lead, participant.first_name, participant.last_name, participant.phone
            )

            # Perform tasks
            after_free_conference_participant_singup(cycle, edition, participant)

            # Redirect to `thank you` page
            return redirect(
                reverse(
                    "core:conference_edition_thanks_page",
                    kwargs={
                        "slug_cycle": cycle.slug,
                        "slug_edition": edition.slug,
                    },
                )
            )
    else:
        form = ConferenceFreeParticipantModelForm()

    return TemplateResponse(
        request,
        template_name,
        {
            "status": status,
            "main_title": edition.title if edition.title else first_schedule.title,
            "cycle": cycle,
            "edition": edition,
            "schedule": schedule,
            "form": form,
            # "is_complex_schedule": is_complex_schedule,
            "lecturers": lecturers,
            "has_started": has_started,
            "first_schedule": first_schedule,
        },
    )


def conference_edition_thanks_page(
    request: HttpRequest, slug_cycle: str, slug_edition: str
):
    """Conference edition thanks page"""
    template_name = "geeks/pages/conference/ConferenceEditionThanksPage.html"
    cycle = get_object_or_404(ConferenceCycle, slug=slug_cycle)
    edition = get_object_or_404(ConferenceEdition, slug=slug_edition)

    webinars = Webinar.manager.get_active_webinars_for_category_slugs(
        [
            *[_.slug for _ in edition.categories.all()],
            *[_.slug for _ in cycle.categories.all()],
        ]
    )

    return TemplateResponse(
        request,
        template_name,
        {
            "cycle": cycle,
            "edition": edition,
            "webinars": webinars,
        },
    )
