from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import (
    Lecturer,
    Webinar,
    WebinarAsset,
    WebinarRecording,
    WebinarRecordingToken,
)
from core.services import StreamingService


def recording_token_page(request: HttpRequest, uuid: str):
    """Recording token page"""
    recording_token = get_object_or_404(WebinarRecordingToken, token=uuid)

    streaming_service = StreamingService(recording_token)
    recording: WebinarRecording = recording_token.recording
    webinar: Webinar = recording.webinar
    webinar: Webinar = recording.webinar
    lecturer: Lecturer = webinar.lecturer
    webinar_assets = WebinarAsset.manager.filter(webinar=webinar).order_by(
        "filename"
    )

    if not streaming_service.is_token_valid():
        template_name = "core/pages/streaming/RecordingTokenExpiredPage.html"
        return TemplateResponse(
            request, template_name, {"uuid": uuid, "recording": recording_token}
        )

    return TemplateResponse(
        request,
        "core/pages/streaming/RecordingTokenPage.html",
        {
            "uuid": uuid,
            "recording": recording_token,
            "webinar": webinar,
            "lecturer": lecturer,
            "webinar_assets": webinar_assets,
        },
    )
