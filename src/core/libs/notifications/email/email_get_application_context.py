from core.models import Lecturer, Webinar, WebinarApplication


def email_get_application_context(application_id: int):
    """Get application context for email"""
    application: WebinarApplication = WebinarApplication.manager.get(
        id=application_id
    )
    webinar: Webinar = application.webinar
    lecturer: Lecturer = webinar.lecturer
    return {
        "application": application,
        "participants": application.participants,
        "webinar": webinar,
        "lecturer": lecturer,
    }
