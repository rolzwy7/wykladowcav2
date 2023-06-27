from django.http import HttpResponse
from django.shortcuts import get_object_or_404
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
from core.tasks import task_send_submitter_confirmation_email
from core.tasks.send_submitter_confirmation_email import create_params

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
    participants = WebinarParticipant.objects.filter(application=application)

    if application.submitter is None:  # TODO: check summary better
        return HttpResponse("Submitter can't be `None`")
    submitter: WebinarApplicationSubmitter = application.submitter

    form = ApplicationSummarySubmitForm()

    if request.method == POST and application.status == ApplicationStatus.INIT:
        form = ApplicationSummarySubmitForm(request.POST)
        if form.is_valid():
            application.status = ApplicationStatus.SENT
            application.save()

            task_send_submitter_confirmation_email.apply_async(
                create_params(submitter.email)
            )

    return TemplateResponse(
        request,
        template_name,
        {**service.get_context(), "participants": participants, "form": form},
    )
