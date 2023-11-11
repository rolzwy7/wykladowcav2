# flake8: noqa:E501
# pylint: disable=line-too-long
from celery import chain, group
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.timezone import now, timedelta

from core.consts import TelegramChats
from core.consts.requests_consts import POST
from core.models import WebinarRecording, WebinarRecordingToken
from core.services import CrmWebinarService
from core.tasks import (
    params_send_participant_recording_email,
    task_send_participant_recording_email,
    task_send_telegram_notification,
)


def crm_send_recording_to_all_participants(request, recording_id: str):
    """Send recording access to all participants of a given webinar"""
    webinar_recording = get_object_or_404(WebinarRecording, recording_id=recording_id)
    crm_webinar_service = CrmWebinarService(webinar_recording.webinar)
    participants = crm_webinar_service.get_gathered_participants()
    webinar_id: int = webinar_recording.webinar.id

    if request.method == POST:
        send_recording_tasks = []

        for participant in participants:
            # Create and save token with participant access
            token = WebinarRecordingToken(
                expires_at=now() + timedelta(hours=48),
                recording=webinar_recording,
                participant=participant,
            )
            token.save()

            # Add task to group
            send_recording_tasks.append(
                task_send_participant_recording_email.si(
                    params_send_participant_recording_email(
                        participant.email,
                        webinar_id,
                        participant.application.id,  # type: ignore
                        reverse(
                            "core:recording_token_page", kwargs={"uuid": token.token}
                        ),
                    )
                )
            )

        chain(
            group(*send_recording_tasks),
            task_send_telegram_notification.si(
                f"Wysłano nagrania do uczestników szkolenia #{webinar_id}",
                TelegramChats.OTHER,
            ),
        ).apply_async()

        return redirect(
            reverse("core:crm_webinar_recordings", kwargs={"pk": webinar_id})
        )

    return TemplateResponse(
        request,
        "core/pages/crm/recording/CrmSendRecordingToAllParticipants.html",
        {
            "recording_id": recording_id,
            "participants": participants,
            "webinar_recording": webinar_recording,
        },
    )
