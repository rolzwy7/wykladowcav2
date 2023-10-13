from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts import POST
from core.models import WebinarApplicationCancellation


def htmx_crm_application_cancellation_toggle(request: HttpRequest, pk: int):
    """Toggle webinar cancellation confirmation"""
    template_path = "htmx/application_toggle_cancellation.html"
    cancellation = get_object_or_404(WebinarApplicationCancellation, pk=pk)

    if request.method == POST:
        cancellation.confirmed = not cancellation.confirmed
        cancellation.save()

    return TemplateResponse(
        request,
        template_path,
        {"cancellation": cancellation},
    )
