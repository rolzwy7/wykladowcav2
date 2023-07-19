from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import POST
from core.forms import CrmAreYouSureForm
from core.models import Webinar
from core.models.enums import WebinarStatus
from core.tasks_dispatch import after_webinar_confirm_dispatch


def crm_webinar_confirm(request, pk: int):
    """Webinar confirmation page"""
    template_name = "core/pages/crm/webinar/CrmWebinarConfirm.html"
    webinar = get_object_or_404(Webinar, pk=pk)

    if webinar.status != WebinarStatus.INIT:
        return HttpResponse("Multiple submit protection triggered")

    if request.method == POST:
        form = CrmAreYouSureForm(request.POST)
        if form.is_valid():
            webinar.status = WebinarStatus.CONFIRMED
            webinar.save()
            after_webinar_confirm_dispatch(webinar)
            return redirect(
                reverse(
                    "core:crm_webinar_detail_dashboard",
                    kwargs={"pk": webinar.pk},
                )
            )
    else:
        form = CrmAreYouSureForm()

    return TemplateResponse(
        request,
        template_name,
        {"webinar": webinar, "form": form},
    )
