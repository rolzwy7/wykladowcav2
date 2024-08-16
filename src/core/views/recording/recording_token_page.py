# flake8: noqa:E501
# pylint: disable=line-too-long

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts.requests_consts import POST
from core.models import (
    Lecturer,
    User,
    Webinar,
    WebinarAsset,
    WebinarRecording,
    WebinarRecordingToken,
)
from core.services import IpAddressService, OpinionsService, StreamingService
from core.services.lecturer import LecturerService


def recording_token_page(request: HttpRequest, uuid: str):
    """Recording token page"""
    recording_token = get_object_or_404(WebinarRecordingToken, token=uuid)
    streaming_service = StreamingService(recording_token)
    if request.user.is_authenticated and request.user.contributor:  # type: ignore
        streaming_service.set_is_contributor(True)

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
    webinar_assets = WebinarAsset.manager.filter(webinar=webinar).order_by("filename")

    lecturer_service = LecturerService(lecturer)
    lecturer_opinions = lecturer_service.get_lecturer_opinions()
    opinions_service = OpinionsService(lecturer_opinions)

    context = {
        "uuid": uuid,
        "recording": recording_token,
        "webinar": webinar,
        "ip_address": IpAddressService.get_client_ip(request),
        "lecturer": lecturer,
        "webinar_assets": webinar_assets,
        "webinar_assets_count": webinar_assets.count(),
        "hide_upper_navbar": False,
        "lecturer_webinars": lecturer_service.get_lecturer_webinars(),
        "nearest_webinar": lecturer_service.get_lecturer_nearest_webinar(),
    }

    if streaming_service.is_free_access():
        return TemplateResponse(
            request,
            "geeks/pages/recordings/RecordingTokenPage.html",
            context,
        )

    if streaming_service.is_password_access():
        if request.method == POST:
            password = request.POST.get("password", "")
            if streaming_service.is_password_correct(password):
                return TemplateResponse(
                    request,
                    "geeks/pages/recordings/RecordingTokenPage.html",
                    context,
                )
            else:
                return TemplateResponse(
                    request,
                    "geeks/pages/recordings/RecordingPasswordFormPage.html",
                    {**context, "password_incorrect": True},
                )
        else:
            return TemplateResponse(
                request,
                "geeks/pages/recordings/RecordingPasswordFormPage.html",
                {**context},
            )

    if streaming_service.is_participant_access():
        participant_email: str = recording_token.participant.email  # type: ignore
        if request.user.is_authenticated:
            user_email: str = request.user.email  # type: ignore
            if streaming_service.is_participant_email_correct(user_email):
                return TemplateResponse(
                    request,
                    "geeks/pages/recordings/RecordingTokenPage.html",
                    context,
                )
            else:
                return TemplateResponse(
                    request,
                    "geeks/pages/recordings/RecordingIncorrectEmailPage.html",
                    {**context, "participant_email": participant_email},
                )
        else:
            participant_email_exists = User.objects.filter(
                email=participant_email
            ).exists()

            if participant_email_exists:
                return TemplateResponse(
                    request,
                    "geeks/pages/recordings/RecordingParticipantEmailExistsPage.html",
                    {**context, "participant_email": participant_email},
                )
            else:
                return TemplateResponse(
                    request,
                    "geeks/pages/recordings/RecordingSimplifiedRegistrationPage.html",
                    {**context, "participant_email": participant_email},
                )

    # Display registration and login instructions
    if not request.user.is_authenticated:
        template_name = "geeks/pages/recordings/RecordingNotLoggedInPage.html"
        return TemplateResponse(request, template_name, {"uuid": uuid})

    return TemplateResponse(
        request,
        "geeks/pages/recordings/RecordingTokenPage.html",
        context,
    )
