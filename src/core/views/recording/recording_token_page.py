from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import WebinarRecordingToken


def recording_token_page(request: HttpRequest, uuid: str):
    """Recording token page"""
    recording = get_object_or_404(WebinarRecordingToken, token=uuid)
    # TODO: token expiration
    template_name = "core/pages/streaming/RecordingTokenPage.html"
    return TemplateResponse(
        request, template_name, {"uuid": uuid, "recording": recording}
    )
