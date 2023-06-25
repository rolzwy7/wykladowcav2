from django.db import transaction
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts.requests_consts import POST
from core.forms import ApplicationInvoiceForm
from core.models import WebinarApplication
from core.models.enums import WebinarApplicationStep
from core.structs import ApplicationStepState


def application_invoice_page(request, uuid: str):
    template_name = "core/pages/application/ApplicationInvoicePage.html"
    application = get_object_or_404(WebinarApplication, uuid=uuid)
    webinar = application.webinar
    invoice = application.invoice  # WebinarApplicationInvoice or None
    state = ApplicationStepState(
        webinar, application, WebinarApplicationStep.INVOICE
    )

    if request.method == POST:
        form = ApplicationInvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            with transaction.atomic():
                invoice = form.save()
                application.invoice = invoice
                application.save()
            return state.get_next_step_redirect()
    else:
        form = ApplicationInvoiceForm(instance=invoice)

    return TemplateResponse(
        request,
        template_name,
        {"form": form, **state.get_context()},
    )
