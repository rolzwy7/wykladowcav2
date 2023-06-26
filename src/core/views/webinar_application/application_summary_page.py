from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts import POST
from core.forms import ApplicationSummarySubmitForm
from core.models import WebinarApplication, WebinarParticipant
from core.models.enums import WebinarApplicationStep
from core.services import ApplicationFormService

APPLICATION_STEP = WebinarApplicationStep.SUMMARY


def application_summary_page(request, uuid):
    template_name = "core/pages/application/ApplicationSummaryPage.html"
    application = get_object_or_404(WebinarApplication, uuid=uuid)
    webinar = application.webinar
    service = ApplicationFormService(
        webinar, application, WebinarApplicationStep.SUMMARY
    )
    service.redirect_on_application_error()

    participants = WebinarParticipant.objects.filter(application=application)

    form = ApplicationSummarySubmitForm()

    if request.method == POST:
        form = ApplicationSummarySubmitForm(request.POST)
        if form.is_valid():
            a = 1  # TODO: Finish this

    return TemplateResponse(
        request,
        template_name,
        {**service.get_context(), "participants": participants, "form": form},
    )
