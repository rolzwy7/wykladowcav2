from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts import POST
from core.forms import DiscountCodeForm
from core.models import WebinarApplication
from core.services import DiscountService


def htmx_application_discount_panel(request: HttpRequest, pk: int):
    """Application discount panel"""
    template_path = "htmx/application_discount_panel.html"
    application = get_object_or_404(WebinarApplication, pk=pk)
    discount_service = DiscountService(application)
    further_discounts_allowed = discount_service.are_further_discounts_allowed()
    error_msg = ""

    if request.method == POST and further_discounts_allowed:
        form = DiscountCodeForm(request.POST)
        if form.is_valid():
            # Get code from form data
            discount_code = form.cleaned_data["discount_code"]

            # Check if code is a ref code
            if discount_service.is_refcode(discount_code):
                discount_service.apply_refcode(discount_code)
            else:
                # If code is not a refcode try to apply normal discount
                discount_valid = discount_service.is_discount_code_valid(
                    discount_code
                )
                if discount_valid:
                    discount_service.create_application_discount_from_code(
                        discount_code
                    )
                else:
                    error_msg = (
                        "Kod jest niepoprawny, wygasł lub już został użyty"
                    )
    else:
        form = DiscountCodeForm()

    # Recalculate is further discounts are allowed
    further_discounts_allowed = discount_service.are_further_discounts_allowed()

    return TemplateResponse(
        request,
        template_path,
        {
            "error_msg": error_msg,
            "form": form,
            "application": application,
            "further_discounts_allowed": further_discounts_allowed,
            **discount_service.get_context(),
        },
    )
