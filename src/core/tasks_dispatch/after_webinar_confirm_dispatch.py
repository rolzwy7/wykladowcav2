from celery import chain, group

from core.models import Webinar, WebinarParticipant
from core.tasks import (
    params_create_clickmeeting_room,
    task_create_clickmeeting_room,
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

    # Dispatch tasks
    chain(
        # Create clickmeeting room
        task_create_clickmeeting_room.s(
            params_create_clickmeeting_room(webinar)
        ),
        # Broadcast `room_id` (int), send invitations for participants
        group(
            *[
                task_send_clickmeeting_invitation_participant.s(
                    participant.email
                )
                for participant in participants
            ]
        ),
        # TODO: Eventlog created clickmeeting room
        # TODO: Eventlog invited - for each participant
    ).apply_async()
