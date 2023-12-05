# flake8: noqa:E501
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import POST
from core.forms import ApplicationSummarySubmitForm
from core.models import Webinar, WebinarApplication, WebinarParticipant
from core.models.enums import ApplicationStatus, WebinarApplicationStep
from core.services import (
    ApplicationFormService,
    ApplicationSummaryService,
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
    # form_service.redirect_on_application_error()
    participants = WebinarParticipant.manager.filter(application=application)

    # Mark `got_to_summary` as True
    if not application.got_to_summary and not request.user.is_staff:
        application.got_to_summary = True
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

            # Send application if user if not staff
            summary_service = ApplicationSummaryService(
                application, request.user, webinar
            )
            summary_service.send_application(dispatch=not request.user.is_staff)

            return redirect(reverse("core:application_success_page"))
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
