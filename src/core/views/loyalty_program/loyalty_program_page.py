# flake8: noqa:E501
# pylint: disable=line-too-long
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.services import LoyaltyProgramService


@login_required(login_url="/logowanie/")
def loyalty_program_terms_of_service_accept_page(request: HttpRequest):
    """Loyalty program terms of service accept page"""
    template_name = (
        "core/pages/loyalty_program/LoyaltyProgramTermsOfServiceAcceptPage.html"
    )
    context = {}
    service = LoyaltyProgramService(request.user)

    if service.loyalty_program_exists_for_user():
        return redirect(reverse("core:loyalty_program_page"))

    if request.POST:
        service.get_or_create_loyalty_program()
        return redirect(reverse("core:loyalty_program_page"))

    return TemplateResponse(request, template_name, context)


@login_required(login_url="/logowanie/")
def loyalty_program_page(request: HttpRequest):
    """Loyalty program page"""
    template_name = "core/pages/loyalty_program/LoyaltyProgramPage.html"
    context = {}
    service = LoyaltyProgramService(request.user)

    if not service.loyalty_program_exists_for_user():
        return redirect(
            reverse("core:loyalty_program_terms_of_service_accept_page")
        )

    return TemplateResponse(request, template_name, context)
