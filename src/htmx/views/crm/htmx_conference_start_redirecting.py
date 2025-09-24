"""htmx_conference_url_form"""

# flake8: noqa=E501

from django.http import HttpRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts import POST
from core.models import ConferenceEdition


def htmx_conference_start_redirecting(request: HttpRequest, pk: int):
    """htmx_conference_start_redirecting"""

    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponseForbidden()

    edition = get_object_or_404(ConferenceEdition, pk=pk)

    if request.method == POST:
        edition.start_redirecting_participants = (
            not edition.start_redirecting_participants
        )
        edition.save()

    return TemplateResponse(
        request,
        "htmx/conference_start_redirecting/result.html",
        {"edition": edition},
    )
