"""Application form summary"""

# flake8: noqa:E501

from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.timezone import now

from core.consts import POST
from core.forms import ApplicationSummarySubmitForm
from core.models import Webinar, WebinarApplication, WebinarParticipant
from core.models.enums import ApplicationStatus, LeadSource, WebinarApplicationStep
from core.services import (
    ApplicationFormService,
    ApplicationSummaryService,
    LeadService,
    LoyaltyProgramService,
)

APPLICATION_STEP = WebinarApplicationStep.SUMMARY


def application_summary_page(request, uuid):
    """Application summary page"""
    template_name = "geeks/pages/application/ApplicationSummaryPage.html"
    application = get_object_or_404(WebinarApplication, uuid=uuid)
    webinar: Webinar = application.webinar
    form_service = ApplicationFormService(
        webinar, application, WebinarApplicationStep.SUMMARY
    )
    participants = WebinarParticipant.manager.get_all_participants_for_application(
        application=application
    )

    # Mark `got_to_summary` as True
    if not application.got_to_summary and not request.user.is_staff:
        application.got_to_summary = True
        application.save()

    if not application.step_dt_summary_start and not request.user.is_staff:
        application.step_dt_summary_start = now()
        application.save()

    if request.method == POST and application.status == ApplicationStatus.INIT:
        form = ApplicationSummarySubmitForm(request.POST)
        if form.is_valid():
            # Create loyalty program income
            if application.refcode:
                provision_user = LoyaltyProgramService.get_user_by_refcode(
                    application.refcode
                )
                if provision_user:
                    loyalty_service = LoyaltyProgramService(provision_user)
                    loyalty_service.create_income_for_application(application)

            # Save participants as leads
            for participant in participants:
                lead = LeadService.get_or_create_lead(
                    participant.email,
                    LeadSource.WEBINAR_PARTICIPANT,
                    request=request,
                    categories=[category for category in webinar.categories.all()],
                )
                LeadService.apply_basic_data(
                    lead,
                    participant.first_name,
                    participant.last_name,
                    participant.phone,
                )

            # Save fallback contact as lead if set
            if application.submitter:
                LeadService.get_or_create_lead(
                    application.submitter.email,
                    LeadSource.WEBINAR_CONTACT,
                    request=request,
                    categories=[category for category in webinar.categories.all()],
                )

            # Send application if user if not staff
            summary_service = ApplicationSummaryService(
                application, request.user, webinar
            )
            summary_service.send_application(dispatch=not request.user.is_staff)

            application.step_dt_summary_end = now()
            application.save()

            return redirect(
                reverse(
                    "core:application_success_page", kwargs={"uuid": application.uuid}
                )
            )
    else:
        form = ApplicationSummarySubmitForm()

    return TemplateResponse(
        request,
        template_name,
        {
            **form_service.get_context(),
            "participants": participants,
            "form": form,
        },
    )
