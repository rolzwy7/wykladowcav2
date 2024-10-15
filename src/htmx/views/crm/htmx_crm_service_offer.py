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
        application.uncertain = not application.uncertain
        application.save()

    return TemplateResponse(
        request,
        template_path,
        {"uncertain": application.uncertain, "application_id": application_id},
    )


def htmx_crm_service_offer_application_toggle_accepted_conditions(
    request: HttpRequest, pk: int
):
    """htmx_crm_service_offer_application_toggle_accepted_conditions"""
    template_path = "htmx/service_offer_application_toggle_accepted_conditions.html"

    application = get_object_or_404(ServiceOfferApplication, pk=pk)
    application_id: int = application.id  # type: ignore

    if request.method == POST:
        application.accepted_conditions = not application.accepted_conditions
        application.save()

    return TemplateResponse(
        request,
        template_path,
        {
            "accepted_conditions": application.accepted_conditions,
            "application_id": application_id,
        },
    )


def htmx_crm_service_offer_application_toggle_resigned(request: HttpRequest, pk: int):
    """htmx_crm_service_offer_application_toggle_resigned"""
    template_path = "htmx/service_offer_application_toggle_resigned.html"

    application = get_object_or_404(ServiceOfferApplication, pk=pk)
    application_id: int = application.id  # type: ignore

    if request.method == POST:
        application.resigned = not application.resigned
        application.save()

    return TemplateResponse(
        request,
        template_path,
        {"resigned": application.resigned, "application_id": application_id},
    )


def htmx_crm_service_offer_application_toggle_no_answer(request: HttpRequest, pk: int):
    """htmx_crm_service_offer_application_toggle_no_answer"""
    template_path = "htmx/service_offer_application_toggle_no_answer.html"

    application = get_object_or_404(ServiceOfferApplication, pk=pk)
    application_id: int = application.id  # type: ignore

    if request.method == POST:
        application.no_answer = not application.no_answer
        application.save()

    return TemplateResponse(
        request,
        template_path,
        {"no_answer": application.no_answer, "application_id": application_id},
    )
