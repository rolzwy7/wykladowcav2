"""HTMX CRM Cancel Webinar"""

# flake8: noqa=E501

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts import POST
from core.models import Webinar
from core.models.enums import WebinarStatus


def htmx_crm_cancel_webinar(request: HttpRequest, pk: int):
    """Cancel Webinar"""
    webinar = get_object_or_404(Webinar, pk=pk)

    if request.method == POST:
        webinar.status = WebinarStatus.CANCELED
        webinar.save()
        return TemplateResponse(
            request,
            "htmx/crm_cancel_webinar_deleted.html",
            {},
        )

    return TemplateResponse(
        request,
        "htmx/crm_cancel_webinar_button.html",
        {"webinar": webinar},
    )
