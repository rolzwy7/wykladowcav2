# flake8: noqa=E501

from django.forms import ModelForm, Select, TextInput
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.timezone import now

from core.consts.requests_consts import POST
from core.models import (
    ConferenceCycle,
    ConferenceEdition,
    ConferenceFreeParticipant,
    ConferenceSchedule,
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
        ]

        widgets = {
            "first_name": TextInput(attrs={"class": "form-control"}),
            "last_name": TextInput(attrs={"class": "form-control"}),
            "voivodeship": Select(attrs={"class": "form-control"}),
            "phone": TextInput(attrs={"class": "form-control"}),
            "email": TextInput(attrs={"class": "form-control"}),
            "know_from": Select(attrs={"class": "form-control"}),
            "using_closed_webinars": Select(attrs={"class": "form-control"}),
        }


def conference_edition_page(request: HttpRequest, slug_cycle: str, slug_edition: str):
    """Conference cycle page"""
    template_name = "geeks/pages/conference/ConferenceEditionPage.html"
    cycle = get_object_or_404(ConferenceCycle, slug=slug_cycle)
    edition = get_object_or_404(ConferenceEdition, slug=slug_edition)
    schedule = ConferenceSchedule.manager.filter(edition=edition).order_by("hour_from")

    # Prepare data
    if schedule.exists():
        is_complex_schedule = schedule.count() > 1
        first_schedule: ConferenceSchedule = schedule.first()  # type: ignore
        main_lecturer = first_schedule.lecturer
        main_title = first_schedule.title
    else:
        main_lecturer = None
        main_title = None
        is_complex_schedule = False
        first_schedule = None  # type: ignore

    has_started = now() > edition.date_from

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
                categories=[_ for _ in cycle.categories.all()],
            )
            LeadService.apply_basic_data(
                lead, participant.first_name, participant.last_name, participant.phone
            )
            # Perform tasks
            after_free_conference_participant_singup(cycle, edition, participant)
            # TODO: Redirect to `thank you` page, spam warning
            return redirect("/")
    else:
        form = ConferenceFreeParticipantModelForm()

    return TemplateResponse(
        request,
        template_name,
        {
            "cycle": cycle,
            "edition": edition,
            "schedule": schedule,
            "form": form,
            "is_complex_schedule": is_complex_schedule,
            "main_title": main_title,
            "main_lecturer": main_lecturer,
            "has_started": has_started,
            "first_schedule": first_schedule,
        },
    )
