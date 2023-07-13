from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts import POST
from core.forms import DiscountCodeForm
from core.models import WebinarApplication
from core.services import DiscountService


def application_discount_panel(request: HttpRequest, pk: int):
    """Application discount panel"""
    template_path = "htmx/application_discount_panel.html"
    application = get_object_or_404(WebinarApplication, pk=pk)
    discount_service = DiscountService(application)
    error_msg = ""

    if request.method == POST:
        form = DiscountCodeForm(request.POST)
        if form.is_valid():
            discount_code = form.cleaned_data["discount_code"]
            discount_valid = discount_service.is_discount_code_valid(
                discount_code
            )
            if discount_valid:
                discount_service.create_application_discount_from_code(
                    discount_code
                )
            else:
                error_msg = "Niepoprawny kod promocyjny"
    else:
        form = DiscountCodeForm()

    return TemplateResponse(
        request,
        template_path,
        {
            "error_msg": error_msg,
            "form": form,
            "application": application,
            **discount_service.get_context(),
        },
    )
