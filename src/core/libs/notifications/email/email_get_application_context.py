# pylint: disable=import-outside-toplevel

from django.urls import reverse

from core.models import WebinarApplication


def email_get_application_context(application_id: int):
    """Get application context for email"""
    application: WebinarApplication = WebinarApplication.manager.get(
        id=application_id
    )
    webinar = application.webinar
    lecturer = webinar.lecturer

    from core.services import ApplicationService

    application_service = ApplicationService(application)

    return {
        "application": application,
        "participants": application_service.get_valid_participants(),
        "webinar": webinar,
        "webinar_url": reverse(
            "core:webinar_redirect_to_program", kwargs={"pk": webinar.id}
        ),
        "lecturer": lecturer,
    }
