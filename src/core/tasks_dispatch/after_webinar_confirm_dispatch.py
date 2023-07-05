from celery import chain, group

from core.models import Lecturer, Webinar, WebinarParticipant
from core.tasks import (
    params_create_clickmeeting_room,
    task_create_clickmeeting_room,
    task_send_clickmeeting_invitation_lecturer,
    task_send_clickmeeting_invitation_participant,
)


def after_webinar_confirm_dispatch(webinar: Webinar):
    """Performs actions after webinar confirmation"""

    # Prepare data
    participants = (
        WebinarParticipant.manager.get_participants_from_sent_applications(
            webinar
        )
    )
    lecturer: Lecturer = webinar.lecturer

    # Dispatch tasks
    clickmeeting_invitations = [
        task_send_clickmeeting_invitation_participant.s(participant.email)
        for participant in participants
    ]

    if lecturer.email:
        clickmeeting_invitations.append(
            task_send_clickmeeting_invitation_lecturer.s(lecturer.email)
        )

    chain(
        # Create clickmeeting room
        task_create_clickmeeting_room.s(
            params_create_clickmeeting_room(webinar)
        ),
        # Broadcast `room_id` (int), send invitations for participants
        group(*clickmeeting_invitations),
    ).apply_async()
