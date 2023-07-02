# pylint: disable=broad-exception-raised

import urllib.parse

import requests
from django.conf import settings

CLICKMEETING_API_URL = settings.CLICKMEETING_API_URL


class ClickmeetingInvitationRole:
    """Clickmeeting role"""

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
    data = f"attendees[0][email]={email}&template=basic&role={role}"
    payload = urllib.parse.quote(data, safe="=&")
    headers = {
        "X-Api-Key": settings.CLICKMEETING_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    result = requests.post(url, data=payload, headers=headers, timeout=10)
    result.raise_for_status()
    if result.json()["status"] != "OK":  # TODO: too broad exception
        raise Exception("response `status` is not OK")
    return result.json()


def send_clickmeeting_invitation_email_to_participant(room_id: str, email: str):
    """Send Clickmeeting invitation email to participant

    Args:
        room_id (str): Room ID
        email (str): email address
    """
    return send_clickmeeting_invitation_email(
        room_id, email, ClickmeetingInvitationRole.LISTENER
    )


def send_clickmeeting_invitation_email_to_lecturer(room_id: str, email: str):
    """Send Clickmeeting invitation email to lecturer

    Args:
        room_id (str): Room ID
        email (str): email address
    """
    return send_clickmeeting_invitation_email(
        room_id, email, ClickmeetingInvitationRole.PRESENTER
    )
