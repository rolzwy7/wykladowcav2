from celery import chain, group
from django.template.defaultfilters import date as _date

from core.consts import TelegramChats
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
            "Wysłano zgłoszenie na szkolenie\n"
            f"Wykładowca: {webinar.lecturer}\n"
            f"Data: {_date(webinar.date, 'j E Y')} "
            f"godz. {_date(webinar.date, 'H:i')}\n"
            f"#{webinar_id}: {webinar.title_original}",
            TelegramChats.APPLICATIONS,
        ),
    ).apply_async()
