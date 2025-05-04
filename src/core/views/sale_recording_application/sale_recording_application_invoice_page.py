"""Application form invoice"""

# flake8: noqa=E501

from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.timezone import now

from core.consts.requests_consts import POST
from core.forms import (
    SaleRecordingApplicationAdditionalInformationForm,
    SaleRecordingApplicationInvoiceForm,
)
from core.models import SaleRecordingApplication, Webinar


def sale_recording_application_invoice_page(request, uuid: str):
    """Application invoice page"""
    template_name = "geeks/pages/sale_recording_application/ApplicationInvoicePage.html"

    application = get_object_or_404(SaleRecordingApplication, uuid=uuid)
    webinar: Webinar = application.sale_recording.recording.webinar

    invoice = application.invoice  # WebinarApplicationInvoice or None

    if request.method == POST:
        form_invoice = SaleRecordingApplicationInvoiceForm(
            request.POST, instance=invoice
        )
        form_additional_info = SaleRecordingApplicationAdditionalInformationForm(
            request.POST, instance=application
        )
        if form_invoice.is_valid() and form_additional_info.is_valid():
            with transaction.atomic():
                application = form_additional_info.save()
                invoice = form_invoice.save()
                application.invoice = invoice
                application.step_invoice_finished = True
                application.step_dt_invoice_end = now()
                application.save()

            return redirect(
                reverse(
                    "core:sale_recording_application_summary_page",
                    kwargs={"uuid": application.uuid},
                )
            )
    else:
        form_invoice = SaleRecordingApplicationInvoiceForm(instance=invoice)
        form_invoice.set_choices(application.application_type)
        form_additional_info = SaleRecordingApplicationAdditionalInformationForm(
            instance=application
        )

    return TemplateResponse(
        request,
        template_name,
        {
            "step_number": 3,
            "step_title": "Faktura",
            "step_description": "Wprowadź dane do faktury",
            "application": application,
            "webinar": webinar,
            "invoice": invoice,
            "form_invoice": form_invoice,
            "form_additional_info": form_additional_info,
        },
    )
