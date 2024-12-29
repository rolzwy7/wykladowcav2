"""HTMX CRM Cancel Webinar"""

# flake8: noqa=E501

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import POST
from core.libs.omega_indexer.request import omega_indexer_request
from core.models import Webinar


def webinar_omega_indexer(request: HttpRequest, pk: int):
    """webinar_omega_indexer"""
    webinar = get_object_or_404(Webinar, pk=pk)

    if request.method == POST:

        if settings.APP_ENV != "production":
            return HttpResponse("nie produkcja")

        absolute_url = settings.BASE_URL + reverse(
            "core:webinar_program_page", kwargs={"slug": webinar.slug}
        )
        response_text = omega_indexer_request(absolute_url, timeout=10)

        return TemplateResponse(
            request,
            "htmx/crm_omega_indexer_queued.html",
            {"response_text": response_text},
        )

    return TemplateResponse(
        request,
        "htmx/crm_omega_indexer_button.html",
        {"webinar": webinar},
    )
