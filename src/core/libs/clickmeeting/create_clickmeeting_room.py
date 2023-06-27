from datetime import datetime
from time import time

import requests
from django.conf import settings
from django.template.defaultfilters import date as _date


def create_clickmeeting_room(
    room_name: str, lobby_description: str, date: datetime, duration: str
) -> int:
    """Creates Clickmeeting room

    Args:
        room_name (str): room name
        lobby_description (str): lobby description
        date (datetime): date
        duration (str): duration

    Returns:
        int: created room id
    """
    url = f"{settings.CLICKMEETING_API_URL}/conferences"
    data = {
        "name": room_name,
        "custom_room_url_name": f"webinar-{int(time())}",
        "room_type": "webinar",
        "permanent_room": False,
        "access_type": "3",  # 3 = Token authentication
        "lobby_description": lobby_description.encode("utf8"),
        "starts_at": _date(date, "Y-m-d H:i:s"),
        "duration": duration,
        "timezone": "Europe/Warsaw",
    }
    headers = {"X-Api-Key": settings.CLICKMEETING_API_KEY}
    result = requests.post(url, data=data, headers=headers, timeout=10)
    result.raise_for_status()
    room_id: int = result.json()["room"]["id"]
    return room_id
