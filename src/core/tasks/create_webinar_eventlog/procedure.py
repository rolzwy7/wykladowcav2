import json

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.models import Webinar, WebinarEventlog


class CreateWebinarEventlogParams(BaseModel):
    """Params"""

    webinar_id: int
    title_html: str
    content_html: str
    icon: str
    color: str


def params(webinar: Webinar) -> str:
    """Create params"""
    json_dump = json.dumps(
        CreateWebinarEventlogParams(
            webinar_id=webinar.id,  # type: ignore
        ).dict()
    )
    return json_dump


def create_webinar_eventlog(
    procedure_params: CreateWebinarEventlogParams,
):
    """Create webinar eventlog"""
    webinar: Webinar = Webinar.manager.get(id=procedure_params.webinar_id)
    eventlog = WebinarEventlog(
        webinar=webinar,
        title_html=procedure_params.title_html,
        content_html=procedure_params.content_html,
        icon=procedure_params.icon,
        color=procedure_params.color,
    )
    eventlog.save()
