# pylint: disable=unused-variable
# pylint: disable=broad-exception-caught
# flake8: noqa:F841

from core.models import Eventlog, Webinar


def eventlog_participant_confirmation_email(webinar_id: int, email: str):
    """Create eventlog when confirmation email has been sent to participant"""
    try:
        title_html = f"[Uczestnik] Wysłano potwierdzenie zgłoszenia: {email}"
        eventlog = Eventlog(
            webinar=Webinar.manager.get(id=webinar_id),
            title_html=title_html,
            icon="user",
            color="success",
        )
        eventlog.save()
    except Exception as exception:
        pass
