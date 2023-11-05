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

    # Recording expired
    if streaming_service.is_token_expired():
        template_name = "geeks/pages/recordings/RecordingExpiredPage.html"
        return TemplateResponse(
            request, template_name, {"uuid": uuid, "recording": recording_token}
        )

    # Recording denied
    if streaming_service.is_access_denied():
        template_name = "geeks/pages/recordings/RecordingDeniedPage.html"
        return TemplateResponse(
            request, template_name, {"uuid": uuid, "recording": recording_token}
        )

    recording: WebinarRecording = recording_token.recording
    webinar: Webinar = recording.webinar
    webinar: Webinar = recording.webinar
    lecturer: Lecturer = webinar.lecturer
    webinar_assets = WebinarAsset.manager.filter(webinar=webinar).order_by(
        "filename"
    )
    context = {
        "uuid": uuid,
        "recording": recording_token,
        "webinar": webinar,
        "ip_address": IpAddressService.get_client_ip(request),
        "lecturer": lecturer,
        "webinar_assets": webinar_assets,
    }

    if streaming_service.is_free_access():
        return TemplateResponse(
            request,
            "geeks/pages/recordings/RecordingTokenPage.html",
            context,
        )

    # TODO: Password access
    # if <password set on recording model instance>:
    #     if <POST>:
    #         get POST.password
    #         if recording model.password == POST.password:
    #             ret video panel
    #         else:
    #             ret display form with error text
    #     else:
    #         ret display form

    # TODO: Simplified registration + login
    # if participant set:
    #     if user authed:
    #         if user.email == participant.email:
    #             ret video panel
    #         else:
    #             ret bad email in user
    #     else:
    #         ret page with button to simplified register

    # Display registration and login instructions
    if not request.user.is_authenticated:
        template_name = "geeks/pages/recordings/RecordingNotLoggedInPage.html"
        return TemplateResponse(request, template_name, {"uuid": uuid})

    return TemplateResponse(
        request,
        "geeks/pages/recordings/RecordingTokenPage.html",
        context,
    )
