# flake8: noqa=E501

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import ConferenceCycle, ConferenceEdition


def conference_edition_page(request: HttpRequest, slug_cycle: str, slug_edition: str):
    """Conference cycle page"""
    template_name = "geeks/pages/conference/ConferenceEditionPage.html"
    cycle = get_object_or_404(ConferenceCycle, slug=slug_cycle)
    edition = get_object_or_404(ConferenceEdition, slug=slug_edition)
    return TemplateResponse(
        request, template_name, {"cycle": cycle, "edition": edition}
    )
