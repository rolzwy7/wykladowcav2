from celery import chain, group

from core.models import Lecturer, Webinar, WebinarParticipant
from core.tasks import (
    params_create_clickmeeting_room,
    params_send_participant_preparation_email,
    task_create_clickmeeting_room,
    task_send_clickmeeting_invitation_lecturer,
    task_send_clickmeeting_invitation_participant,
    task_send_participant_preparation_email,
    task_send_telegram_notification,
)


def after_webinar_confirm_dispatch(webinar: Webinar):
    """Performs actions after webinar confirmation"""

    # Prepare data
    webinar_id: int = webinar.id  # type: ignore
    participants = (
        WebinarParticipant.manager.get_participants_from_sent_applications(
            webinar
        )
    )
    lecturer: Lecturer = webinar.lecturer

    # Send ClickMeeting invitation to all application's participants
    clickmeeting_invitations = [
        task_send_clickmeeting_invitation_participant.s(participant.email)
        for participant in participants
    ]

    # If Lecturer's email is set then send host invitation
    if lecturer.email:
        clickmeeting_invitations.append(
            task_send_clickmeeting_invitation_lecturer.s(lecturer.email)
        )

    # Send preparation email to all participants along with invitation
    preparation_emails = [
        task_send_participant_preparation_email.si(
            params_send_participant_preparation_email(
                participant.email, webinar
            )
        )
        for participant in participants
    ]

    # Dispatch tasks
    chain(
        # Create clickmeeting room
        task_create_clickmeeting_room.s(
            params_create_clickmeeting_room(webinar)
        ),
        # Broadcast `room_id` (int), send invitations for participants
        group(*clickmeeting_invitations),
        group(*preparation_emails),
        task_send_telegram_notification.si(
            f"Termin szkolenia #{webinar_id} został potwierdzony"
        ),
    ).apply_async()
