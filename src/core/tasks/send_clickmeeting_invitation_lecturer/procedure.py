from core.libs.clickmeeting import (
    send_clickmeeting_invitation_email_to_lecturer,
)


def send_clickmeeting_invitation_lecturer(room_id: int, email: str):
    """Send clickmeeting invitation lecturer"""
    return send_clickmeeting_invitation_email_to_lecturer(
        room_id=str(room_id),
        email=email,
    )
