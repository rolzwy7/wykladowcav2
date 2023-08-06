# flake8: noqa:E501
# pylint: disable=line-too-long
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import POST
from core.forms import LoyaltyPayoutRequestForm
from core.services import LoyaltyProgramService


@login_required(login_url="/logowanie/")
def loyalty_program_terms_of_service_accept_page(request: HttpRequest):
    """Loyalty program terms of service accept page"""
    template_name = (
        "core/pages/loyalty_program/LoyaltyProgramTermsOfServiceAcceptPage.html"
    )
    context = {}
    service = LoyaltyProgramService(request.user)  # type: ignore

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
    service = LoyaltyProgramService(request.user)  # type: ignore

    # Check if loyalty program exists
    if not service.loyalty_program_exists_for_user():
        return redirect(
            reverse("core:loyalty_program_terms_of_service_accept_page")
        )
    else:
        loyalty_program = service.get_or_create_loyalty_program()

    # Payout form handling
    if request.method == POST:
        form = LoyaltyPayoutRequestForm(request.POST)
        if form.is_valid():
            a = 1
    else:
        form = LoyaltyPayoutRequestForm()

    context = {
        "ref_code": loyalty_program.ref_number,
        "incomes": service.get_user_incomes(),
        "form": form,
    }

    return TemplateResponse(request, template_name, context)
