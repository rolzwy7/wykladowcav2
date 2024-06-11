"""
Conference edition pages
"""

# flake8: noqa=E501

from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts.requests_consts import POST
from core.forms import ConferenceFreeParticipantModelForm
from core.models import ConferenceEdition, ConferenceFreeParticipant, Webinar
from core.services import ConferenceService
from core.tasks_dispatch import after_free_conference_participant_singup


def conference_edition_page(request: HttpRequest, slug_edition: str):
    """Conference cycle page"""
    template_name = "geeks/pages/conference/ConferenceEditionPage.html"
    edition = ConferenceService.get_edition_or_404_by_slug(slug_edition)
    service = ConferenceService(edition)

    # Handle form submission
    if request.method == POST:

        form = ConferenceFreeParticipantModelForm(request.POST)
        if form.is_valid():

            # Perform actions on free participant submit
            participant = service.on_free_participant_submit(request, form)

            # Perform tasks
            after_free_conference_participant_singup(service.edition, participant)

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
            "webinar": service.webinar,
            "edition": edition,
            "status": service.get_edition_status(),
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
    service = ConferenceService(edition)

    if edition.stream_url_page:
        return redirect(edition.stream_url_page)

    return TemplateResponse(
        request,
        template_name,
        {
            "free_participant": free_participant,
            "edition": edition,
            "webinar": service.webinar,
            "status": service.get_edition_status(),
            "watch_token": watch_token,
            "hide_footer_newsletter_singup": True,
        },
    )
