from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts.requests_consts import POST
from core.forms import ApplicationSubmitterForm
from core.models import WebinarApplication


def application_submitter_page(request, uuid: str):
    template_name = "core/pages/application/ApplicationSubmitterPage.html"
    application = get_object_or_404(WebinarApplication, uuid=uuid)
    webinar = application.webinar
    submitter = application.submitter  # None or WebinarApplicationSubmitter

    if request.method == POST:
        form = ApplicationSubmitterForm(request.POST, instance=submitter)
        if form.is_valid():
            return redirect(
                reverse(
                    "core:???",
                    kwargs={"uuid": application.uuid},
                )
            )
    else:
        form = ApplicationSubmitterForm(instance=submitter)

    return TemplateResponse(
        request,
        template_name,
        {"webinar": webinar, "application": application, "form": form},
    )
