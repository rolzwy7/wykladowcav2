"""sale_recording_process_webhook_dispatch_tasks procedure"""

# flake8: noqa=E501
# pylint: disable=import-outside-toplevel

from celery import chain
from django.conf import settings
from django.urls import reverse
from django.utils.timezone import now, timedelta

from core.consts import TelegramChats
from core.models import (
    SaleRecordingApplication,
    SaleRecordingParticipant,
    WebinarRecordingToken,
)


def sale_recording_process_webhook_dispatch_tasks(invoice_proforma_id: int):
    """Process sale recording webhook"""

    from core.tasks import (
        params_sale_recording_send_access_email,
        task_sale_recording_send_access_email,
        task_send_telegram_notification,
    )

    applications = SaleRecordingApplication.manager.filter(
        fakturownia_invoice_id=str(invoice_proforma_id)
    )

    if not applications.exists():
        return "APPLICATION_DOESNT_EXIST"

    application: SaleRecordingApplication = applications.first()  # type: ignore
    application_id: int = application.id  # type: ignore

    # Send access to recording
    task_chain = []
    participants = SaleRecordingParticipant.manager.filter(application=application)
    for participant in participants:
        token = WebinarRecordingToken(
            expires_at=now() + timedelta(days=14),
            recording=application.sale_recording.recording,
        )
        token.save()

        token_path = reverse("core:recording_token_page", kwargs={"uuid": token.token})
        access_url = f"{settings.BASE_URL}{token_path}"

        task_chain.append(
            task_sale_recording_send_access_email.si(
                access_url,
                params_sale_recording_send_access_email(
                    participant.email, application_id
                ),
            )
        )

        telegram_msg = (
            f"{participant.first_name} {participant.last_name} <{participant.email}>"
        )
        task_chain.append(
            task_send_telegram_notification.si(
                telegram_msg,
                TelegramChats.OTHER,
            )
        )

    chain(*task_chain).apply_async()

    # TODO: Wyslij certyfikaty
