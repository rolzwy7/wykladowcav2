import json

from core.libs.fakturownia import InvoiceCreateResult
from core.models import WebinarApplication, WebinarApplicationMetadata
from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app


@app.task(name="save_application_invoice_metadata", base=BaseTaskWithRetry)
def task_save_application_invoice_metadata(
    invoice_result_json: str, application_id: int
):
    """Task for `save_application_invoice_metadata`"""
    invoice_result = InvoiceCreateResult(**json.loads(invoice_result_json))
    application = WebinarApplication.manager.get(id=application_id)
    metadata, _ = WebinarApplicationMetadata.objects.get_or_create(
        application=application
    )

    # Save metadata
    metadata.invoice_id = str(invoice_result.invoice_id)
    metadata.invoice_number = invoice_result.invoice_number
    metadata.invoice_url = invoice_result.invoice_view_url
    metadata.save()
