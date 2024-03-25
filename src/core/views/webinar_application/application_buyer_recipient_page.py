"""Application buyer-recipient form"""

# flake8: noqa=E501

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.timezone import now

from core.consts import POST
from core.forms import ApplicationBuyerForm, ApplicationRecipientForm
from core.models import WebinarApplication
from core.models.enums import WebinarApplicationStep
from core.services import ApplicationFormService


def application_buyer_recipient_page(request, uuid: str):
    """Application recipient page"""
    template_name = "geeks/pages/application/ApplicationBuyerRecipientPage.html"
    application = get_object_or_404(WebinarApplication, uuid=uuid)

    # Get webinar, buyer and recipient
    webinar = application.webinar
    recipient = application.recipient
    buyer = application.buyer

    application_form_service = ApplicationFormService(
        webinar, application, WebinarApplicationStep.RECIPIENT
    )
    application_form_service.redirect_on_application_error()

    if request.method == POST:
        form_buyer = ApplicationBuyerForm(request.POST, prefix="buyer", instance=buyer)
        form_recipient = ApplicationRecipientForm(
            request.POST, prefix="recipient", instance=recipient
        )

        if form_buyer.is_valid() or form_recipient.is_valid():
            with transaction.atomic():
                recipient = form_recipient.save()
                buyer = form_buyer.save()
                application.recipient = recipient
                application.buyer = buyer
                ApplicationFormService.create_submitter(
                    application, buyer.phone_number, buyer.email
                )
                application.step_buyer_finished = True
                application.step_recipient_finished = True
                application.step_dt_buyer_end = now()
                application.step_dt_recipient_end = now()
                application.save()
            return application_form_service.get_next_step_redirect()
    else:
        form_buyer = ApplicationBuyerForm(prefix="buyer", instance=buyer)
        form_recipient = ApplicationRecipientForm(
            prefix="recipient", instance=recipient
        )
        if not application.step_dt_recipient_start:
            application.step_dt_recipient_start = now()
            application.save()

    return TemplateResponse(
        request,
        template_name,
        {
            "form_recipient": form_recipient,
            "form_buyer": form_buyer,
            **application_form_service.get_context(),
        },
    )
