"""Create free ClickMeeting room"""

# flake8: noqa=E501

import urllib.parse
from datetime import datetime
from time import time

import requests
from django.conf import settings
from django.template.defaultfilters import date as _date
from django.utils.timezone import get_default_timezone

CLICKMEETING_API_URL = settings.CLICKMEETING_API_URL
CLICKMEETING_API_KEY = settings.CLICKMEETING_API_KEY


def create_free_clickmeeting_room(
    room_name: str, lobby_description: str, date: datetime, duration: str
) -> tuple[int, str]:
    """Creates Clickmeeting room

    Args:
        room_name (str): room name
        lobby_description (str): lobby description
        date (datetime): date
        duration (str): duration

    Returns:
        int: created room id
    """
    tz = get_default_timezone()
    url = f"{CLICKMEETING_API_URL}/conferences"
    custom_room_url_name = f"konferencja-{int(time())}"
    data = {
        "name": room_name,
        "custom_room_url_name": custom_room_url_name,
        "room_type": "webinar",
        "permanent_room": False,
        "access_type": "1",  # 1 = open access room
        "lobby_description": lobby_description.encode("utf8"),
        "starts_at": _date(date.astimezone(tz), "Y-m-d H:i:s"),  # apply timezone
        "duration": duration,
        "timezone": "Europe/Warsaw",
    }
    payload = urllib.parse.urlencode(data)
    headers = {
        "X-Api-Key": CLICKMEETING_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    result = requests.post(url, data=payload, headers=headers, timeout=10)
    result.raise_for_status()
    room_id: int = result.json()["room"]["id"]
    return room_id, f"{settings.CLICKMEETING_DOMAIN}/{custom_room_url_name}"
