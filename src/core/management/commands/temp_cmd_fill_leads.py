"""
Temporary command - fill leads with participants
"""

# flake8: noqa=E501

from django.core.management.base import BaseCommand

from core.models import Webinar, WebinarApplication, WebinarParticipant
from core.models.enums import LeadSource
from core.services import LeadService


class Command(BaseCommand):
    """temp_cmd_fill_leads"""

    def handle(self, *args, **options):
        lead_service = LeadService()

        applications = WebinarApplication.manager.all()
        for application in applications:
            webinar: Webinar = application.webinar
            if not application.submitter:
                continue
            #
            first_name = application.submitter.first_name
            last_name = application.submitter.last_name
            email = application.submitter.email
            phone = application.submitter.phone
            #
            lead = lead_service.get_or_create_lead(
                email,
                LeadSource.WEBINAR_CONTACT,
                categories=[_ for _ in webinar.categories.all()],
            )
            lead_service.apply_basic_data(lead, first_name, last_name, phone)
            print(lead)

            participants = (
                WebinarParticipant.manager.get_all_participants_for_application(
                    application
                )
            )
            for participant in participants:
                email = participant.email
                first_name = participant.first_name
                last_name = participant.last_name
                phone = participant.phone
                lead = lead_service.get_or_create_lead(
                    email,
                    LeadSource.WEBINAR_PARTICIPANT,
                    categories=[_ for _ in webinar.categories.all()],
                )
                lead_service.apply_basic_data(lead, first_name, last_name, phone)
                print(lead)
