"""Application form buyer"""

# flake8: noqa=E501

from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import POST
from core.forms import SaleRecordingApplicationBuyerForm
from core.models import SaleRecordingApplication, Webinar


def sale_recording_application_buyer_page(request, uuid: str):
    """Application buyer page"""
    template_name = "geeks/pages/sale_recording_application/ApplicationBuyerPage.html"
    application = get_object_or_404(SaleRecordingApplication, uuid=uuid)
    webinar: Webinar = application.sale_recording.recording.webinar
    buyer = application.buyer

    if request.method == POST:
        form = SaleRecordingApplicationBuyerForm(
            request.POST, prefix="buyer", instance=buyer
        )
        if form.is_valid():
            with transaction.atomic():
                buyer = form.save()
                application.buyer = buyer
                # application.step_buyer_finished = True
                # application.step_dt_buyer_end = now()
                application.save()
            return redirect(
                reverse(
                    "core:sale_recording_application_participants_page",
                    kwargs={"uuid": application.uuid},
                )
            )
    else:
        form = SaleRecordingApplicationBuyerForm(
            instance=buyer,
            prefix="buyer",
            initial={
                "phone_number": settings.COMPANY_OFFICE_PHONE,
            },
        )

    return TemplateResponse(
        request,
        template_name,
        {
            "form": form,
            "application": application,
            "webinar": webinar,
            "step_number": 1,
            "step_description": "Wprowadź dane Nabywcy",
            "step_title": "Nabywca",
            "previous_step_url": reverse(
                "core:sale_recording_application_type_page", kwargs={"pk": webinar.pk}
            ),
        },
    )
