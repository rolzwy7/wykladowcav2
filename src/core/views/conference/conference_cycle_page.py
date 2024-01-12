"""
Conference cycle page
"""

# flake8: noqa=E501

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import ConferenceCycle, ConferenceEdition


def conference_cycle_page(request: HttpRequest, slug_cycle: str):
    """Conference cycle page"""
    template_name = "geeks/pages/conference/ConferenceCyclePage.html"
    cycle = get_object_or_404(ConferenceCycle, slug=slug_cycle)

    # Get editions sorted by start date (asc)
    editions = ConferenceEdition.manager.get_active_editions_for_cycle(
        cycle=cycle
    ).order_by("date_from")

    # Nearest edition
    nearset_edition = editions[:1]

    return TemplateResponse(
        request,
        template_name,
        {"cycle": cycle, "editions": editions, "nearset_edition": nearset_edition},
    )
