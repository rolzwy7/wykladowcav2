from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import ConferenceCycle, ConferenceEdition


def conference_cycle_page(request: HttpRequest, slug_cycle: str):
    """Conference cycle page"""
    template_name = "geeks/pages/conference/ConferenceCyclePage.html"
    cycle = get_object_or_404(ConferenceCycle, slug=slug_cycle)
    editions = ConferenceEdition.manager.filter(cycle=cycle)
    return TemplateResponse(
        request, template_name, {"cycle": cycle, "editions": editions}
    )
