from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import WebinarRecordingToken
from core.services import StreamingService


def recording_token_page(request: HttpRequest, uuid: str):
    """Recording token page"""
    template_name = "core/pages/streaming/RecordingTokenPage.html"

    recording_token = get_object_or_404(WebinarRecordingToken, token=uuid)

    streaming_service = StreamingService(recording_token)

    if not streaming_service.is_token_valid():
        template_name = "core/pages/streaming/RecordingTokenExpiredPage.html"
        return TemplateResponse(
            request, template_name, {"uuid": uuid, "recording": recording_token}
        )

    return TemplateResponse(
        request, template_name, {"uuid": uuid, "recording": recording_token}
    )
