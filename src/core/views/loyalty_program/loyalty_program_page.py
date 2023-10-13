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
    template_name = "geeks/pages/loyalty_program/LoyaltyProgramTermsOfServiceAcceptPage.html"
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
    template_name = "geeks/pages/loyalty_program/LoyaltyProgramPage.html"
    service = LoyaltyProgramService(request.user)  # type: ignore
    error = ""

    # Check if loyalty program exists
    if not service.loyalty_program_exists_for_user():
        return redirect(
            reverse("core:loyalty_program_terms_of_service_accept_page")
        )
    else:
        loyalty_program = service.get_or_create_loyalty_program()
        service.mark_payed_as_payable()

    # Payout form handling
    if request.method == POST:
        form = LoyaltyPayoutRequestForm(request.POST, request.FILES)
        if form.is_valid():
            payout_brutto = form.cleaned_data["payout_brutto"]
            success, msg = service.can_create_payout_value(payout_brutto)
            if not success:
                error = msg
            else:
                payout = form.save(commit=False)
                payout.loyalty_program = loyalty_program
                payout.save()
                return redirect(
                    f'{reverse("core:loyalty_program_page")}?payout_saved=1'
                )
    else:
        form = LoyaltyPayoutRequestForm()

    context = {
        **service.get_context(),
        "form": form,
        "error": error,
        "payout_saved": request.GET.get("payout_saved", ""),
    }

    return TemplateResponse(request, template_name, context)
