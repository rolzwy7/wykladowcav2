from typing import Optional

from core.models import CrmTodo, Webinar, WebinarApplication


def create_crm_todo(
    title: str,
    html: str,
    icon: str,
    color: str,
    url: str,
    webinar_id: Optional[int] = None,
    application_id: Optional[int] = None,
):
    """Create CRM To-Do"""

    if webinar_id:
        webinar = Webinar.manager.get(id=webinar_id)
    else:
        webinar = None

    if application_id:
        application = WebinarApplication.manager.get(id=application_id)
    else:
        application = None

    CrmTodo(
        title=title,
        html=html,
        icon=icon,
        color=color,
        url=url,
        webinar=webinar,
        application=application,
    ).save()
