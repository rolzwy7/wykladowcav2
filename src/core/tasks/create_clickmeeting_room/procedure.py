import json

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.clickmeeting import (
    create_clickmeeting_room as lib_create_clickmeeting_room,
)
from core.libs.eventlog import eventlog_clickmeeting_room_created
from core.models import Webinar, WebinarMetadata
from core.models.enums import WEBINAR_CLICKMEETING_DURATION


class CreateClickmeetingRoomParams(BaseModel):
    """Params"""

    webinar_id: int


def params(webinar: Webinar) -> str:
    """Create params"""
    json_dump = json.dumps(
        CreateClickmeetingRoomParams(
            webinar_id=webinar.id,  # type: ignore
        ).dict()
    )
    return json_dump


def create_clickmeeting_room(
    procedure_params: CreateClickmeetingRoomParams,
) -> int:
    """Create clickmeeting room and save it's ID to webinar metadata"""

    webinar: Webinar = Webinar.manager.get(id=procedure_params.webinar_id)

    room_id = lib_create_clickmeeting_room(
        room_name=webinar.title,
        lobby_description=webinar.program,
        date=webinar.date,
        duration=WEBINAR_CLICKMEETING_DURATION[webinar.duration],
    )

    # Save Clickmeeting room id into webinar metadata
    metadata, _ = WebinarMetadata.objects.get_or_create(webinar=webinar)
    metadata.clickmeeting_id = str(room_id)
    metadata.save()

    eventlog_clickmeeting_room_created(webinar)

    return room_id
