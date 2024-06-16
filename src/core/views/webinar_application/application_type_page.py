"""Application form type"""

# flake8: noqa:E501
# pylint: disable=line-too-long

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts import POST
from core.forms import ApplicationTypeForm
from core.models import (
    Webinar,
    WebinarApplication,
    WebinarApplicationMetadata,
    WebinarApplicationTracking,
)
from core.services import (
    ApplicationFormService,
    DiscountService,
    IpAddressService,
    ReflinkService,
)


def application_type_page(request, pk: int):
    """Controller for webinar application form page - application type form"""
    template_name = "geeks/pages/application/ApplicationTypePage.html"
    webinar = get_object_or_404(Webinar, pk=pk)
    reflink_service = ReflinkService(request)
    tracking_code = request.session.get("tracking_code", "no_code")

    # Create application tracking if set
    if tracking_code != "no_code":
        WebinarApplicationTracking(webinar=webinar, tracking_code=tracking_code).save()

    if request.method == POST:
        form = ApplicationTypeForm(request.POST)
        if form.is_valid():
            # TODO: move this to service ?? reflink_service would be a dependancy

            with transaction.atomic():
                # Create apllication
                application = WebinarApplication(
                    application_type=form.cleaned_data["application_type"],
                    price_netto=webinar.price,
                    price_old=webinar.price_netto,
                    webinar=webinar,
                )

                # Set tracking code
                application.tracking_code = tracking_code

                # Set reflink
                if reflink_service.is_refcode_valid():
                    refcode = reflink_service.get_ref_code()
                    application.refcode = refcode

                # Save spplication
                application.save()

                # If webinar is discounted apply discount
                discount_service = DiscountService(application)
                discount_service.maybe_apply_initial_application_discount()

            metadata = WebinarApplicationMetadata.objects.get(application=application)
            metadata.ip_address = IpAddressService.get_client_ip(request)
            metadata.save()

            return ApplicationFormService.get_application_type_redirect(
                application.application_type, application.uuid
            )
    else:
        form = ApplicationTypeForm()

    return TemplateResponse(
        request,
        template_name,
        {
            "step_number": "1",
            "step_title": "Typ zgłoszenia",
            "step_description": "Wybierz czy wysyłasz zgłoszenie jako Firma, JSFP lub Osoba Prywatna",
            "application_timeline": [("Typ zgłoszenia", "-", True)],
            "webinar": webinar,
            "form": form,
            "show_pdf_card_alert": request.GET.get("pdf", ""),
        },
    )
