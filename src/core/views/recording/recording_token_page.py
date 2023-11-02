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
from core.services import IpAddressService, StreamingService


def recording_token_page(request: HttpRequest, uuid: str):
    """Recording token page"""
    recording_token = get_object_or_404(WebinarRecordingToken, token=uuid)
    streaming_service = StreamingService(recording_token)

    if streaming_service.is_access_denied():
        template_name = "geeks/pages/recordings/RecordingDeniedPage.html"
        return TemplateResponse(
            request, template_name, {"uuid": uuid, "recording": recording_token}
        )

    if streaming_service.is_token_expired():
        template_name = "geeks/pages/recordings/RecordingExpiredPage.html"
        return TemplateResponse(
            request, template_name, {"uuid": uuid, "recording": recording_token}
        )

    # Display login instructions
    if not request.user.is_authenticated:
        template_name = "geeks/pages/recordings/RecordingNotLoggedInPage.html"
        return TemplateResponse(request, template_name, {"uuid": uuid})

    recording: WebinarRecording = recording_token.recording
    webinar: Webinar = recording.webinar
    webinar: Webinar = recording.webinar
    lecturer: Lecturer = webinar.lecturer
    webinar_assets = WebinarAsset.manager.filter(webinar=webinar).order_by(
        "filename"
    )

    return TemplateResponse(
        request,
        "geeks/pages/recordings/RecordingTokenPage.html",
        {
            "uuid": uuid,
            "recording": recording_token,
            "webinar": webinar,
            "ip_address": IpAddressService.get_client_ip(request),
            "lecturer": lecturer,
            "webinar_assets": webinar_assets,
        },
    )
