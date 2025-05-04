# pylint: disable=import-outside-toplevel

# flake8: noqa

from django.urls import reverse

from core.models import (
    SaleRecordingApplication,
    SaleRecordingParticipant,
    WebinarApplication,
)


def email_get_application_context(application_id: int):
    """Get application context for email"""
    application: WebinarApplication = WebinarApplication.manager.get(id=application_id)
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


def sale_recording_email_get_application_context(application_id: int):
    """Get application context for email"""
    application: SaleRecordingApplication = SaleRecordingApplication.manager.get(
        id=application_id
    )
    webinar = application.sale_recording.recording.webinar
    lecturer = webinar.lecturer

    participants = SaleRecordingParticipant.manager.filter(application=application)

    return {
        "application": application,
        "participants": participants,
        "webinar": webinar,
        "webinar_url": reverse(
            "core:webinar_redirect_to_program", kwargs={"pk": webinar.id}
        ),
        "lecturer": lecturer,
    }
