from celery import chain

from core.models import (
    WebinarApplication,
    WebinarApplicationSubmitter,
    WebinarParticipant,
)
from core.tasks import (
    params_send_participant_confirmation_email,
    params_send_submitter_confirmation_email,
    task_send_participant_confirmation_email,
    task_send_submitter_confirmation_email,
    task_send_telegram_notification,
)


def after_application_sent_dispatch(
    application: WebinarApplication, submitter: WebinarApplicationSubmitter
):
    """Dispatch tasks after application sent"""

    # Prepare data
    participants = WebinarParticipant.manager.filter(application=application)
    webinar_id: int = application.webinar.id

    # Dispatch tasks
    chain(
        task_send_submitter_confirmation_email.si(
            params_send_submitter_confirmation_email(
                submitter.email,
                webinar_id,
            )
        ),
        *[
            task_send_participant_confirmation_email.si(
                params_send_participant_confirmation_email(
                    participant.email, webinar_id
                )
            )
            for participant in participants
        ],
        task_send_telegram_notification.si("Wysłano zgłoszenie na szkolenie")
    ).apply_async()
