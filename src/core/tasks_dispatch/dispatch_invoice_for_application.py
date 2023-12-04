# flake8: noqa:E501
# pylint: disable=line-too-long
# pylint: disable=import-outside-toplevel
from celery import chain

from core.models import WebinarApplication
from core.tasks import (
    task_create_application_invoice,
    task_save_application_invoice_metadata,
    task_send_invoice_email,
)


def dispatch_invoice_for_application(
    application: WebinarApplication, send_via_email: bool = True
):
    """Dispatch invoice for given application"""

    from core.services import ApplicationService

    application_service = ApplicationService(application)

    # Prevent blank invoice from being created
    if application_service.get_valid_participants().count() == 0:
        return

    invoice_jobs = [
        task_create_application_invoice.si(application.id),  # type: ignore
        task_save_application_invoice_metadata.s(application.id),  # type: ignore
    ]

    if send_via_email:
        invoice_jobs.append(
            task_send_invoice_email.si(application.invoice.invoice_email, application.id),  # type: ignore
        )

    # Dispatch invoice tasks
    chain(*invoice_jobs).apply_async()
