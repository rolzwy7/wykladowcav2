from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts import POST
from core.forms import CrmAreYouSureForm
from core.models import Webinar
from core.models.enums import WebinarStatus


def crm_webinar_done(request, pk: int):
    """Webinar done page"""
    template_name = "core/pages/crm/webinar/CrmWebinarDone.html"
    webinar = get_object_or_404(Webinar, pk=pk)

    if request.method == POST:
        form = CrmAreYouSureForm(request.POST)
        if form.is_valid():
            webinar.status = WebinarStatus.DONE
            webinar.save()
    else:
        form = CrmAreYouSureForm()

    return TemplateResponse(
        request,
        template_name,
        {"webinar": webinar, "form": form},
    )
