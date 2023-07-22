# flake8: noqa:E501
# pylint: disable=line-too-long

from core.models import (
    Webinar,
    WebinarApplication,
    WebinarApplicationCancellation,
    WebinarApplicationSubmitter,
)
from core.tasks import (
    params_send_submitter_cancellation_email,
    task_send_submitter_cancellation_email,
)


def after_webinar_cancel_dispatch(webinar: Webinar):
    """Performs actions after webinar cancellation"""

    # Prepare data
    webinar_id: int = webinar.id  # type: ignore
    sent_applications = WebinarApplication.manager.sent_applications(webinar)

    # For each sent application
    for sent_application in sent_applications:
        sent_application_id: int = sent_application.id  # type: ignore

        # Create application cancellation object
        application_cancellation = WebinarApplicationCancellation(
            application=sent_application
        )
        application_cancellation.save()

        # Send cancellation e-mail to submitter
        submitter: WebinarApplicationSubmitter = sent_application.submitter  # type: ignore
        task_send_submitter_cancellation_email.si(
            params_send_submitter_cancellation_email(
                submitter.email,
                webinar_id,
                sent_application_id,
                str(application_cancellation.token),
            )
        ).apply_async()
