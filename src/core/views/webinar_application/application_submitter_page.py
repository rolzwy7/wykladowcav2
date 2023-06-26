from django.db import transaction
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts.requests_consts import POST
from core.forms import ApplicationSubmitterForm
from core.models import WebinarApplication
from core.models.enums import WebinarApplicationStep
from core.services import ApplicationFormService


def application_submitter_page(request, uuid: str):
    """Application submitter page"""
    template_name = "core/pages/application/ApplicationSubmitterPage.html"
    application = get_object_or_404(WebinarApplication, uuid=uuid)
    webinar = application.webinar
    submitter = application.submitter  # None or WebinarApplicationSubmitter
    service = ApplicationFormService(
        webinar, application, WebinarApplicationStep.SUBMITTER
    )
    service.redirect_on_application_error()

    if request.method == POST:
        form = ApplicationSubmitterForm(request.POST, instance=submitter)
        if form.is_valid():
            with transaction.atomic():
                submitter = form.save()
                application.submitter = submitter
                application.save()
                service.save_submitter_as_participant(application, submitter)
            return service.get_next_step_redirect()
    else:
        form = ApplicationSubmitterForm(instance=submitter)

    return TemplateResponse(
        request,
        template_name,
        {"form": form, **service.get_context()},
    )
