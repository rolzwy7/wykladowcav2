from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts.requests_consts import POST
from core.forms import ApplicationAdditionalInformationForm
from core.models import WebinarApplication
from core.models.enums import WebinarApplicationStep
from core.services import ApplicationFormService


def application_additional_information_page(request, uuid):
    """Additional info form page"""
    template_name = "geeks/pages/application/AdditionalInformationPage.html"
    application = get_object_or_404(WebinarApplication, uuid=uuid)
    webinar = application.webinar
    state = ApplicationFormService(
        webinar, application, WebinarApplicationStep.ADDITIONAL_INFO
    )

    if request.method == POST:
        form = ApplicationAdditionalInformationForm(
            request.POST, instance=application
        )
        if form.is_valid():
            application = form.save()
            return state.get_next_step_redirect()
    else:
        form = ApplicationAdditionalInformationForm(instance=application)

    return TemplateResponse(
        request,
        template_name,
        {"form": form, **state.get_context()},
    )
