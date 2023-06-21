from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts.requests_consts import POST
from core.forms import ApplicationBuyerForm
from core.models import WebinarApplication


def application_buyer_page(request, uuid: str):
    template_name = "core/pages/application/ApplicationBuyerPage.html"
    application = get_object_or_404(WebinarApplication, uuid=uuid)
    webinar = application.webinar
    buyer = application.buyer  # None or WebinarApplicationCompany

    if request.method == POST:
        form = ApplicationBuyerForm(request.POST, instance=buyer)
        if form.is_valid():
            return redirect(
                reverse(
                    "core:application_invoice_page",
                    kwargs={"uuid": application.uuid},
                )
            )
    else:
        form = ApplicationBuyerForm(instance=buyer)

    return TemplateResponse(
        request,
        template_name,
        {"webinar": webinar, "application": application, "form": form},
    )
