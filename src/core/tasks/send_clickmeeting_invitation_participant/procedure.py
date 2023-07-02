from core.libs.clickmeeting import (
    send_clickmeeting_invitation_email_to_participant,
)


def send_clickmeeting_invitation_participant(room_id: int, email: str):
    """Send clickmeeting invitation"""
    return send_clickmeeting_invitation_email_to_participant(
        room_id=str(room_id),
        email=email,
    )
