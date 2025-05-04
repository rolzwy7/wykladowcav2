"""Application form private person"""

# flake8: noqa=E501

from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import VAT_EXEMPTION_0
from core.consts.requests_consts import POST
from core.forms import SaleRecordingApplicationPersonDetailForm
from core.models import (
    SaleRecordingApplication,
    SaleRecordingApplicationInvoice,
    SaleRecordingParticipant,
    Webinar,
)


def sale_recording_application_person_details_page(request, uuid: str):
    """Application private person page"""
    template_name = (
        "geeks/pages/sale_recording_application/ApplicationPersonDetailsPage.html"
    )

    application = get_object_or_404(SaleRecordingApplication, uuid=uuid)
    webinar: Webinar = application.sale_recording.recording.webinar

    private_person = application.private_person  # WebinarApplicationInvoice or None

    if request.method == POST:
        form = SaleRecordingApplicationPersonDetailForm(
            request.POST, instance=private_person
        )
        if form.is_valid():
            with transaction.atomic():
                private_person = form.save()
                application.private_person = private_person

                ##########

                # Save participant
                # Delete all participants and save new one
                SaleRecordingParticipant.manager.filter(
                    application=application
                ).delete()
                SaleRecordingParticipant(
                    application=application,
                    first_name=private_person.first_name,
                    last_name=private_person.last_name,
                    email=private_person.email,
                ).save()

                # Save invoice
                if application.invoice:
                    invoice = application.invoice
                    invoice.invoice_email = private_person.email
                    invoice.save()
                else:
                    vat_exemption = VAT_EXEMPTION_0.db_key
                    invoice = SaleRecordingApplicationInvoice(
                        vat_exemption=vat_exemption,
                        invoice_email=private_person.email,
                    )
                    application.invoice = invoice  # type: ignore
                    invoice.save()

                ##########

                application.save()

            return redirect(
                reverse(
                    "core:sale_recording_application_summary_page",
                    kwargs={"uuid": application.uuid},
                )
            )
    else:
        form = SaleRecordingApplicationPersonDetailForm(instance=private_person)

    return TemplateResponse(
        request,
        template_name,
        {
            "application": application,
            "webinar": webinar,
            "form": form,
            "step_number": 1,
            "step_description": "Wprowadź swoje dane",
            "step_title": "Osoba prywatna",
        },
    )
