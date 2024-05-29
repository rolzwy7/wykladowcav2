"""Conference service"""

# flake8: noqa=E501

from django.db import transaction
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from core.forms import ConferenceFreeParticipantModelForm
from core.models import ConferenceFreeParticipant, Webinar
from core.models.conference import ConferenceEdition
from core.models.enums import LeadSource

from .lead_service import LeadService


class ConferenceService:
    """ConferenceService"""

    def __init__(self, edition: ConferenceEdition):
        self.edition = edition
        self.webinar: Webinar = edition.webinar

    @staticmethod
    def get_edition_or_404_by_slug(slug: str):
        """Get edition by slug or 404"""
        edition = get_object_or_404(ConferenceEdition, slug=slug)
        return edition

    def get_edition_status(self):
        """Get calculated status for this edition"""
        if now() < self.webinar.date:
            return "WAITING"
        elif now() >= self.webinar.date_end:
            return "FINISHED"
        else:
            return "IN_PROGRESS"

    def on_free_participant_submit(
        self, request: HttpRequest, form: ConferenceFreeParticipantModelForm
    ):
        """Action on free participant submit"""

        with transaction.atomic():

            # Save free participant with form
            participant: ConferenceFreeParticipant = form.save(commit=False)
            participant.edition = self.edition
            participant.save()

            # Save lead
            lead = LeadService.get_or_create_lead(
                participant.email,
                LeadSource.CONFERENCE_FREE,
                request=request,
                categories=list(self.webinar.categories.all()),
            )
            LeadService.apply_basic_data(
                lead, participant.first_name, participant.last_name, participant.phone
            )

        return participant
