"""htmx_crm_participant_toggle_uncertain"""

# flake8: noqa=E501
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts import POST
from core.models import ServiceOfferApplication


def htmx_crm_service_offer_application_toggle_uncertain(request: HttpRequest, pk: int):
    """htmx_crm_service_offer_application_toggle_uncertain"""
    template_path = "htmx/service_offer_application_toggle_uncertain.html"

    application = get_object_or_404(ServiceOfferApplication, pk=pk)
    application_id: int = application.id  # type: ignore

    if request.method == POST:
        ServiceOfferApplication.manager.filter(id=application_id).update(
            uncertain=not application.uncertain
        )

    return TemplateResponse(
        request,
        template_path,
        {"is_uncertain": not application.uncertain, "application_id": application_id},
    )
