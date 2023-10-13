import json

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.models import Eventlog, Webinar


class CreateEventlogParams(BaseModel):
    """Params"""

    webinar_id: int
    title_html: str
    content_html: str
    icon: str
    color: str


def params(
    webinar: Webinar,
    title_html: str,
    content_html: str,
    icon: str,
    color: str,
) -> str:
    """Create params"""
    webinar_id: int = webinar.id  # type: ignore
    json_dump = json.dumps(
        CreateEventlogParams(
            webinar_id=webinar_id,
            title_html=title_html,
            content_html=content_html,
            icon=icon,
            color=color,
        ).dict()
    )
    return json_dump


def create_eventlog(
    procedure_params: CreateEventlogParams,
):
    """Create webinar eventlog"""
    webinar: Webinar = Webinar.manager.get(id=procedure_params.webinar_id)
    eventlog = Eventlog(
        webinar=webinar,
        title_html=procedure_params.title_html,
        content_html=procedure_params.content_html,
        icon=procedure_params.icon,
        color=procedure_params.color,
    )
    eventlog.save()
