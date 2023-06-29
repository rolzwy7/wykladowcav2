import requests
from django.conf import settings

CLICKMEETING_API_URL = settings.CLICKMEETING_API_URL


class ClickmeetingInvitationRole:
    LISTENER = "listener"
    PRESENTER = "presenter"


def send_clickmeeting_invitation_email(room_id: str, email: str, role: str):
    """Send Clickmeeting invitation email

    Args:
        room_id (str): Room ID
        email (str): email address
        role (str): invite as role ('listener' or 'presenter')
    """
    lang = "pl"
    url = (
        f"{CLICKMEETING_API_URL}/conferences/{room_id}/invitation/email/{lang}"
    )
    data = {"attendees": [email], "template": "basic", "role": role}
    headers = {"X-Api-Key": settings.CLICKMEETING_API_KEY}
    result = requests.post(url, data=data, headers=headers, timeout=10)
    result.raise_for_status()


def send_clickmeeting_invitation_email_to_participant(room_id: str, email: str):
    """Send Clickmeeting invitation email to participant

    Args:
        room_id (str): Room ID
        email (str): email address
    """
    send_clickmeeting_invitation_email(
        room_id, email, ClickmeetingInvitationRole.LISTENER
    )


def send_clickmeeting_invitation_email_to_lecturer(room_id: str, email: str):
    """Send Clickmeeting invitation email to lecturer

    Args:
        room_id (str): Room ID
        email (str): email address
    """
    send_clickmeeting_invitation_email(
        room_id, email, ClickmeetingInvitationRole.PRESENTER
    )
