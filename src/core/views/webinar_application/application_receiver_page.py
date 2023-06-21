from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts.requests_consts import POST
from core.forms import ApplicationReceiverForm
from core.models import WebinarApplication


def application_receiver_page(request, uuid: str):
    template_name = "core/pages/application/ApplicationReceiverPage.html"
    application = get_object_or_404(WebinarApplication, uuid=uuid)
    webinar = application.webinar

    if request.method == POST:
        form = ApplicationReceiverForm(request.POST)
        if form.is_valid():
            ...
    else:
        form = ApplicationReceiverForm()

    return TemplateResponse(
        request, template_name, {"webinar": webinar, "form": form}
    )
