from core.models import Lecturer, Webinar, WebinarApplication
from core.services import ApplicationService


def email_get_application_context(application_id: int):
    """Get application context for email"""
    application: WebinarApplication = WebinarApplication.manager.get(
        id=application_id
    )
    webinar: Webinar = application.webinar
    lecturer: Lecturer = webinar.lecturer
    application_service = ApplicationService(application)

    return {
        "application": application,
        "participants": application_service.get_valid_participants(),
        "webinar": webinar,
        "lecturer": lecturer,
    }
