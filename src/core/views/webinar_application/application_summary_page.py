# flake8: noqa:E501
from typing import Optional

from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from core.consts import POST
from core.forms import ApplicationSummarySubmitForm
from core.models import (
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
    webinar = application.webinar
    service = ApplicationFormService(
        webinar, application, WebinarApplicationStep.SUMMARY
    )
    service.redirect_on_application_error()
    participants = WebinarParticipant.manager.filter(application=application)

    # Double check that submitter is set, typing is confused ant thinks that
    # `submitter` is `Never`
    if not application.submitter:
        return redirect(service.get_first_step_url())
    submitter: WebinarApplicationSubmitter = application.submitter  # type: ignore

    if request.method == POST and application.status == ApplicationStatus.INIT:
        form = ApplicationSummarySubmitForm(request.POST)
        if form.is_valid():
            after_application_sent_dispatch(application, submitter)
            application.status = ApplicationStatus.SENT
            application.save()
            return redirect(reversed("core:application_success_page"))
    else:
        form = ApplicationSummarySubmitForm()

    return TemplateResponse(
        request,
        template_name,
        {**service.get_context(), "participants": participants, "form": form},
    )
