from celery import chain, group

from core.models import (
    Webinar,
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
    webinar: Webinar = application.webinar
    webinar_id: int = webinar.id  # type: ignore
    application_id: int = application.id  # type: ignore

    # Dispatch tasks
    chain(
        group(
            task_send_submitter_confirmation_email.si(
                params_send_submitter_confirmation_email(
                    submitter.email,
                    webinar_id,
                    application_id,
                )
            ),
            *[
                task_send_participant_confirmation_email.si(
                    params_send_participant_confirmation_email(
                        participant.email,
                        webinar_id,
                        application_id,
                    )
                )
                for participant in participants
            ],
        ),
        task_send_telegram_notification.si(
            f"Wysłano zgłoszenie na szkolenie #{webinar_id}"
        ),
    ).apply_async()
