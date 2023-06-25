from django.db import transaction
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts.requests_consts import POST
from core.forms import ApplicationPersonDetailForm
from core.models import WebinarApplication
from core.models.enums import WebinarApplicationStep
from core.structs import ApplicationStepState
from core.utils.application import populate_private_person_data


def application_person_details_page(request, uuid: str):
    template_name = "core/pages/application/ApplicationPersonDetailsPage.html"
    application = get_object_or_404(WebinarApplication, uuid=uuid)
    webinar = application.webinar
    private_person = (
        application.private_person
    )  # WebinarApplicationInvoice or None
    state = ApplicationStepState(
        webinar, application, WebinarApplicationStep.PERSON_DETAILS
    )

    if request.method == POST:
        form = ApplicationPersonDetailForm(
            request.POST, instance=private_person
        )
        if form.is_valid():
            with transaction.atomic():
                private_person = form.save()
                application.private_person = private_person
                populate_private_person_data(application, private_person)
                application.save()

            return state.get_next_step_redirect()
    else:
        form = ApplicationPersonDetailForm(instance=private_person)

    return TemplateResponse(
        request,
        template_name,
        {"form": form, **state.get_context()},
    )
