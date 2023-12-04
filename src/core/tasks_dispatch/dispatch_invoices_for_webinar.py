# flake8: noqa:E501
# pylint: disable=line-too-long
# pylint: disable=import-outside-toplevel
from celery import chain, group

from core.models import Webinar, WebinarApplication
from core.tasks import (
    task_create_application_invoice,
    task_save_application_invoice_metadata,
    task_send_invoice_email,
)


def dispatch_invoices_for_webinar(webinar: Webinar, send_via_email: bool = True):
    """Dispatch invoices for given webinar"""

    from core.services import ApplicationService

    applications = WebinarApplication.manager.sent_applications_for_webinar(webinar)

    # Create invoice jobs
    invoice_jobs = []
    for application in applications:
        application_service = ApplicationService(application)

        # Prevent blank invoices from being created
        if application_service.get_valid_participants().count() == 0:
            continue

        tasks_seq = [
            task_create_application_invoice.si(application.id),  # type: ignore
            task_save_application_invoice_metadata.s(application.id),  # type: ignore
        ]

        if send_via_email:
            tasks_seq.append(
                task_send_invoice_email.si(application.invoice.invoice_email, application.id),  # type: ignore
            )

        invoice_jobs.append(chain(*tasks_seq))

    # Dispatch invoice tasks
    group(*invoice_jobs).apply_async()
