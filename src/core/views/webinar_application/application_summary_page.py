# flake8: noqa:E501
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import POST
from core.forms import ApplicationSummarySubmitForm
from core.models import (
    Webinar,
    WebinarApplication,
    WebinarApplicationSubmitter,
    WebinarParticipant,
)
from core.models.enums import ApplicationStatus, WebinarApplicationStep
from core.services import ApplicationFormService
from core.tasks_dispatch import after_application_sent_dispatch

APPLICATION_STEP = WebinarApplicationStep.SUMMARY


def application_summary_page(request, uuid):
    """Application summary page"""
    template_name = "core/pages/application/ApplicationSummaryPage.html"
    application = get_object_or_404(WebinarApplication, uuid=uuid)
    webinar: Webinar = application.webinar
    form_service = ApplicationFormService(
        webinar, application, WebinarApplicationStep.SUMMARY
    )
    form_service.redirect_on_application_error()
    participants = WebinarParticipant.manager.filter(application=application)

    # TODO: This is working but it's kinda sad. Why `submitter` is `Never` ???
    # Double check that submitter is set, typing is confused and thinks that
    # `submitter` is `Never`
    if not application.submitter:
        return redirect(form_service.get_first_step_url())
    submitter: WebinarApplicationSubmitter = application.submitter  # type: ignore

    if request.method == POST and application.status == ApplicationStatus.INIT:
        form = ApplicationSummarySubmitForm(request.POST)
        if form.is_valid():
            # Set application status as changed
            application.status = ApplicationStatus.SENT

            # If user authenticated then connect
            if request.user.is_authenticated:
                application.user = request.user

            # Decrement webinar's remaining places
            webinar.remaining_places = max(0, webinar.remaining_places - 1)

            # Dispatch tasks after application send
            after_application_sent_dispatch(application, submitter)

            # Save changes
            application.save()
            webinar.save()

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
