from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts.requests_consts import POST
from core.forms import ApplicationInvoiceForm
from core.models import WebinarApplication


def application_invoice_page(request, uuid: str):
    template_name = "core/pages/application/ApplicationInvoicePage.html"
    application = get_object_or_404(WebinarApplication, uuid=uuid)
    webinar = application.webinar

    if request.method == POST:
        form = ApplicationInvoiceForm(request.POST)
        if form.is_valid():
            return redirect(
                reverse(
                    "core:application_submitter_page",
                    kwargs={"uuid": application.uuid},
                )
            )
    else:
        form = ApplicationInvoiceForm()

    return TemplateResponse(
        request,
        template_name,
        {"webinar": webinar, "application": application, "form": form},
    )
