from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import POST
from core.forms import ApplicationTypeForm
from core.models import Webinar, WebinarApplication


def application_type_page(request, pk: int):
    template_name = "core/pages/application/ApplicationTypePage.html"
    webinar = get_object_or_404(Webinar, pk=pk)

    if request.method == POST:
        form = ApplicationTypeForm(request.POST)
        if form.is_valid():
            application = WebinarApplication(
                application_type=form.cleaned_data["application_type"],
                price_netto=webinar.price_netto,
                webinar=webinar,
            )
            application.save()
            return redirect(
                reverse(
                    "core:application_buyer_page",
                    kwargs={"uuid": application.uuid},
                )
            )
    else:
        form = ApplicationTypeForm()

    return TemplateResponse(
        request, template_name, {"webinar": webinar, "form": form}
    )
