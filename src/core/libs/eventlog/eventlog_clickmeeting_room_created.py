# pylint: disable=unused-variable
# pylint: disable=broad-exception-caught
# flake8: noqa:F841

from django.urls import reverse

from core.models import Eventlog, Webinar

from .eventlog_utils import create_link


def eventlog_clickmeeting_room_created(webinar: Webinar):
    """Create eventlog when Clickmeeting room is created"""
    try:
        webinar_id: int = webinar.id  # type: ignore
        link = create_link(
            f"#{webinar_id}",
            reverse(
                "core:crm_webinar_detail_dashboard", kwargs={"pk": webinar_id}
            ),
        )
        title_html = f"Stworzono pokój w Clickmeeting dla webinaru {link}"
        eventlog = Eventlog(
            webinar=webinar,
            title_html=title_html,
            content_html=f"SNIPPET:CLICKMEETING_ROOM:{webinar_id}",
            icon="youtube",
            color="success",
        )
        eventlog.save()
    except Exception as exception:
        pass
