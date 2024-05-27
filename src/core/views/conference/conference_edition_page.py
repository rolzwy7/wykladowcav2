"""
Conference edition pages
"""

# flake8: noqa=E501

from django.forms import CheckboxInput, ModelForm, Select, TextInput
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts.requests_consts import POST
from core.models import ConferenceEdition, ConferenceFreeParticipant, Webinar
from core.models.enums import LeadSource
from core.services.lead_service import LeadService
from core.tasks_dispatch import after_free_conference_participant_singup


class ConferenceFreeParticipantModelForm(ModelForm):
    """ConferenceFreeParticipantModelForm"""

    class Meta:
        """meta"""

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


def conference_edition_page(request: HttpRequest, slug_edition: str):
    """Conference cycle page"""
    template_name = "geeks/pages/conference/ConferenceEditionPage.html"
    edition = get_object_or_404(ConferenceEdition, slug=slug_edition)
    webinar: Webinar = edition.webinar

    # Handle form submission
    if request.method == POST:

        # TODO: move this
        form = ConferenceFreeParticipantModelForm(request.POST)
        if form.is_valid():

            # TODO Transaction ?

            # Save free participant with form
            participant: ConferenceFreeParticipant = form.save(commit=False)
            participant.edition = edition
            participant.save()

            # Save lead
            lead = LeadService.get_or_create_lead(
                participant.email,
                LeadSource.CONFERENCE_FREE,
                request=request,
                categories=list(webinar.categories.all()),
            )
            LeadService.apply_basic_data(
                lead, participant.first_name, participant.last_name, participant.phone
            )

            # Perform tasks
            after_free_conference_participant_singup(edition, participant)

            # Redirect to `thank you` page
            return redirect(
                reverse(
                    "core:conference_edition_thanks_page",
                    kwargs={
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
            "webinar": webinar,
            "edition": edition,
            "form": form,
            "hide_footer_newsletter_singup": True,
        },
    )


def conference_edition_thanks_page(request: HttpRequest, slug_edition: str):
    """Conference edition thanks page"""
    template_name = "geeks/pages/conference/ConferenceEditionThanksPage.html"
    edition = get_object_or_404(ConferenceEdition, slug=slug_edition)
    webinar: Webinar = edition.webinar

    webinars = Webinar.manager.get_active_webinars_for_category_slugs(
        list(webinar.categories.all())
    )

    return TemplateResponse(
        request,
        template_name,
        {
            "edition": edition,
            "webinars": webinars,
            "hide_footer_newsletter_singup": True,
        },
    )


def conference_edition_waiting_room_page(request: HttpRequest, watch_token: str):
    """conference_waiting_room_page"""
    template_name = "geeks/pages/conference/ConferenceEditionWaitingRoom.html"
    free_participant = get_object_or_404(
        ConferenceFreeParticipant, watch_token=watch_token
    )
    edition: ConferenceEdition = free_participant.edition
    webinar: Webinar = edition.webinar

    # TODO: Adres IP ?

    return TemplateResponse(
        request,
        template_name,
        {
            "free_participant": free_participant,
            "edition": edition,
            "webinar": webinar,
            "hide_footer_newsletter_singup": True,
        },
    )
