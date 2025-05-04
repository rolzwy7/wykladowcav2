"""Application form type"""

# flake8: noqa:E501
# pylint: disable=line-too-long

from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import POST
from core.forms import SaleRecordingApplicationTypeForm
from core.models import SaleRecording, SaleRecordingApplication
from core.services import IpAddressService


def sale_recording_application_type_page(request, pk: int):
    """Controller for webinar application form page - application type form"""
    template_name = "geeks/pages/sale_recording_application/ApplicationTypePage.html"
    sale_recording = get_object_or_404(SaleRecording, pk=pk)
    webinar = sale_recording.recording.webinar
    # reflink_service = ReflinkService(request)
    tracking_code = request.session.get("tracking_code", "no_code")
    campaign_id = request.session.get("campaign_id", "no_campaign_id")

    # # Create application tracking if set
    # if tracking_code != "no_code":
    #     tracking_obj = WebinarApplicationTracking(
    #         webinar=webinar, tracking_code=tracking_code
    #     )
    #     # Save from which campaign the application was sent
    #     if campaign_id != "no_campaign_id":
    #         tracking_obj.campaign_id = campaign_id
    #     tracking_obj.save()

    if request.method == POST:
        form = SaleRecordingApplicationTypeForm(request.POST)
        if form.is_valid():

            with transaction.atomic():
                # Create apllication
                application = SaleRecordingApplication(
                    application_type=form.cleaned_data["application_type"],
                    price_netto=webinar.price,
                    price_old=webinar.price_netto,
                    sale_recording=sale_recording,
                )

                # Set tracking code
                application.tracking_code = tracking_code
                application.campaign_id = campaign_id

                # Set IP address
                application.ip_address = IpAddressService.get_client_ip(request)

                # # Set reflink
                # if reflink_service.is_refcode_valid():
                #     refcode = reflink_service.get_ref_code()
                #     application.refcode = refcode

                # Save spplication
                application.save()

                # # If webinar is discounted apply discount
                # discount_service = DiscountService(application)
                # discount_service.maybe_apply_initial_application_discount()

            redirect_path_name = {
                "COMPANY": "sale_recording_application_buyer_page",
                "JSFP": "sale_recording_application_buyer_recipient_page",
                "PRIVATE_PERSON": "sale_recording_application_person_details_page",
            }[application.application_type]
            return redirect(
                reverse(f"core:{redirect_path_name}", kwargs={"uuid": application.uuid})
            )
    else:
        form = SaleRecordingApplicationTypeForm()

    return TemplateResponse(
        request,
        template_name,
        {
            "step_number": "1",
            "step_title": "Typ zgłoszenia",
            "step_description": "Wybierz czy wysyłasz zgłoszenie jako Firma, JSFP lub Osoba Prywatna",
            "application_timeline": [("Typ zgłoszenia", "-", True)],
            "sale_recording": sale_recording,
            "webinar": webinar,
            "form": form,
        },
    )
