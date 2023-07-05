from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts import POST
from core.forms import ApplicationSummarySubmitForm
from core.models import WebinarApplication, WebinarParticipant
from core.models.enums import ApplicationStatus, WebinarApplicationStep
from core.services import ApplicationFormService
from core.tasks_dispatch import after_application_sent_dispatch

APPLICATION_STEP = WebinarApplicationStep.SUMMARY


def application_summary_page(request, uuid):
    """Application summary page"""
    template_name = "core/pages/application/ApplicationSummaryPage.html"
    application = get_object_or_404(WebinarApplication, uuid=uuid)
    submitter = application.submitter
    webinar = application.webinar
    service = ApplicationFormService(
        webinar, application, WebinarApplicationStep.SUMMARY
    )
    service.redirect_on_application_error()
    participants = WebinarParticipant.manager.filter(application=application)

    form = ApplicationSummarySubmitForm()

    if request.method == POST and application.status == ApplicationStatus.INIT:
        form = ApplicationSummarySubmitForm(request.POST)
        if form.is_valid():
            after_application_sent_dispatch(application, submitter)
            application.status = ApplicationStatus.SENT
            application.save()

    return TemplateResponse(
        request,
        template_name,
        {**service.get_context(), "participants": participants, "form": form},
    )
