import json
from datetime import datetime

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.clickmeeting import (
    create_clickmeeting_room as lib_create_clickmeeting_room,
)
from core.libs.notifications.email import EmailMessage, EmailTemplate


class CreateClickmeetingRoomParams(BaseModel):
    """Params"""

    room_name: str
    lobby_description: str
    date: datetime
    duration: str


def params(email: str) -> str:
    """Create params"""
    json_dump = json.dumps(CreateClickmeetingRoomParams(email=email).dict())
    return json_dump


def create_clickmeeting_room(
    procedure_params: CreateClickmeetingRoomParams,
):
    """Create clickmeeting room"""
    lib_create_clickmeeting_room(
        procedure_params.room_name,
        procedure_params.lobby_description,
        procedure_params.date,
        procedure_params.duration,
    )
