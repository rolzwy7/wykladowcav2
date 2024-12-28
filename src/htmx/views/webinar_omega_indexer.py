"""HTMX CRM Cancel Webinar"""

# flake8: noqa=E501

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts import POST
from core.models import Webinar
from core.models.enums import WebinarStatus


def webinar_omega_indexer(request: HttpRequest, pk: int):
    """webinar_omega_indexer"""
    webinar = get_object_or_404(Webinar, pk=pk)

    if request.method == POST:
        # TODO: Mark webinar as queued in omega indexer
        # TODO: Queue in Omega Indexer
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
