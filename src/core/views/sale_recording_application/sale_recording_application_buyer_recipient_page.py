"""Application buyer-recipient form"""

# flake8: noqa=E501

from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.timezone import now

from core.consts import POST
from core.forms import (
    SaleRecordingApplicationBuyerForm,
    SaleRecordingApplicationRecipientForm,
)
from core.models import SaleRecordingApplication, Webinar


def sale_recording_application_buyer_recipient_page(request, uuid: str):
    """Application recipient page"""
    template_name = (
        "geeks/pages/sale_recording_application/ApplicationBuyerRecipientPage.html"
    )

    application = get_object_or_404(SaleRecordingApplication, uuid=uuid)
    webinar: Webinar = application.sale_recording.recording.webinar

    # Get webinar, buyer and recipient
    recipient = application.recipient
    buyer = application.buyer

    if request.method == POST:
        form_buyer = SaleRecordingApplicationBuyerForm(
            request.POST, prefix="buyer", instance=buyer
        )
        form_recipient = SaleRecordingApplicationRecipientForm(
            request.POST, prefix="recipient", instance=recipient
        )

        if form_buyer.is_valid() or form_recipient.is_valid():
            with transaction.atomic():
                recipient = form_recipient.save()
                buyer = form_buyer.save()
                application.recipient = recipient
                application.buyer = buyer
                application.save()
            return redirect(
                reverse(
                    "core:sale_recording_application_participants_page",
                    kwargs={"uuid": application.uuid},
                )
            )
    else:
        form_buyer = SaleRecordingApplicationBuyerForm(
            prefix="buyer",
            instance=buyer,
            initial={
                "phone_number": settings.COMPANY_OFFICE_PHONE,
            },
        )
        form_recipient = SaleRecordingApplicationRecipientForm(
            prefix="recipient", instance=recipient
        )

    return TemplateResponse(
        request,
        template_name,
        {
            "application": application,
            "webinar": webinar,
            "step_number": 1,
            "step_description": "Wprowadź dane Nabywcy i Odbiorcy",
            "step_title": "Nabywca i Odbiorca",
            "form_recipient": form_recipient,
            "form_buyer": form_buyer,
        },
    )
