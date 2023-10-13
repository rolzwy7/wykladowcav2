from django.db import transaction
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import POST
from core.forms import ApplicationBuyerForm
from core.models import WebinarApplication
from core.models.enums import WebinarApplicationStep
from core.services import ApplicationFormService


def application_buyer_page(request, uuid: str):
    """Application buyer page"""
    template_name = "geeks/pages/application/ApplicationBuyerPage.html"
    application = get_object_or_404(WebinarApplication, uuid=uuid)
    webinar = application.webinar
    buyer = application.buyer
    service = ApplicationFormService(
        webinar, application, WebinarApplicationStep.BUYER
    )
    service.redirect_on_application_error()

    if request.method == POST:
        form = ApplicationBuyerForm(
            request.POST, prefix="buyer", instance=buyer
        )
        if form.is_valid():
            with transaction.atomic():
                buyer = form.save()
                application.buyer = buyer
                ApplicationFormService.create_submitter(
                    application, buyer.phone_number, buyer.email
                )
                application.save()
            return service.get_next_step_redirect()
    else:
        form = ApplicationBuyerForm(instance=buyer, prefix="buyer")

    return TemplateResponse(
        request,
        template_name,
        {
            "form": form,
            "previous_step_url": reverse(
                "core:application_type_page", kwargs={"pk": webinar.pk}
            ),
            **service.get_context(),
        },
    )
