from django.db import transaction
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts.requests_consts import POST
from core.forms import (
    ApplicationAdditionalInformationForm,
    ApplicationInvoiceForm,
)
from core.models import WebinarApplication
from core.models.enums import WebinarApplicationStep
from core.services import ApplicationFormService


def application_invoice_page(request, uuid: str):
    """Application invoice page"""
    template_name = "geeks/pages/application/ApplicationInvoicePage.html"
    application = get_object_or_404(WebinarApplication, uuid=uuid)
    webinar = application.webinar
    invoice = application.invoice  # WebinarApplicationInvoice or None
    service = ApplicationFormService(
        webinar, application, WebinarApplicationStep.INVOICE
    )
    # service.redirect_on_application_error()

    if request.method == POST:
        form_invoice = ApplicationInvoiceForm(request.POST, instance=invoice)
        form_additional_info = ApplicationAdditionalInformationForm(
            request.POST, instance=application
        )
        if form_invoice.is_valid() and form_additional_info.is_valid():
            with transaction.atomic():
                application = form_additional_info.save()
                invoice = form_invoice.save()
                application.invoice = invoice
                application.save()

            return service.get_next_step_redirect()
    else:
        form_invoice = ApplicationInvoiceForm(instance=invoice)
        form_invoice.set_choices(application.application_type)
        form_additional_info = ApplicationAdditionalInformationForm(
            instance=application
        )

    return TemplateResponse(
        request,
        template_name,
        {
            "form_invoice": form_invoice,
            "form_additional_info": form_additional_info,
            **service.get_context(),
        },
    )
