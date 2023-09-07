from django.db import transaction
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts.requests_consts import POST
from core.forms import ApplicationInvoiceForm
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
    service.redirect_on_application_error()

    if request.method == POST:
        form = ApplicationInvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            with transaction.atomic():
                invoice = form.save()
                application.invoice = invoice
                application.save()
            return service.get_next_step_redirect()
    else:
        form = ApplicationInvoiceForm(instance=invoice)
        form.set_choices(application.application_type)

    return TemplateResponse(
        request,
        template_name,
        {"form": form, **service.get_context()},
    )
