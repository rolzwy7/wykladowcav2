from celery import group

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
)


def after_application_sent_dispatch(
    application: WebinarApplication, submitter: WebinarApplicationSubmitter
):
    """Dispatch tasks after application sent"""

    # Prepare data
    participants = WebinarParticipant.objects.filter(application=application)

    job = group(
        task_send_submitter_confirmation_email.s(
            params_send_submitter_confirmation_email(submitter.email)
        ),
        *[
            task_send_participant_confirmation_email.s(
                params_send_participant_confirmation_email(participant.email)
            )
            for participant in participants
        ],
    )

    job.apply_async()
