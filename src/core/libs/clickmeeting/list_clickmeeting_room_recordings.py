# pylint: disable=no-name-in-module

import requests
from django.conf import settings
from pydantic import BaseModel

CLICKMEETING_API_URL = settings.CLICKMEETING_API_URL
CLICKMEETING_API_KEY = settings.CLICKMEETING_API_KEY


class ListClickmeetingRoomRecordingsResponse(BaseModel):
    """Represents response for result from REGON Api"""

    id: int  # 4284611,
    recording_url: str  # "https://recorder-eu-1...
    recording_duration: int  # 1292,
    recorder_started: str  # "2023-06-26 07:56:31",
    recorder_start_date: str  # "2023-06-26T07:56:31+00:00",
    recording_file_size: str  # "183812200",
    recording_name: str  # "Kontrola PIP po zmianach Kodeksu Pracy w 2023 r."


def list_clickmeeting_room_recordings(
    room_id: int,
) -> list[ListClickmeetingRoomRecordingsResponse]:
    """List all recordings for given Clickmeeting Room ID"""

    response = requests.get(
        f"{CLICKMEETING_API_URL}/conferences/{room_id}/recordings",
        timeout=(10, 10),
        headers={"X-Api-Key": CLICKMEETING_API_KEY},
    )
    response.raise_for_status()

    return [
        ListClickmeetingRoomRecordingsResponse(**recording)
        for recording in response.json()
    ]
