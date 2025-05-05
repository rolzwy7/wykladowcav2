"""sale_recording_save_application_invoice_metadata"""

# flake8: noqa=E501

import json

from core.libs.fakturownia import ProformaInvoiceCreateResult
from core.models import SaleRecordingApplication
from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app


@app.task(
    name="sale_recording_save_application_invoice_metadata", base=BaseTaskWithRetry
)
def task_sale_recording_save_application_invoice_metadata(
    invoice_result_json: str, application_id: int
):
    """Task for `sale_recording_save_application_invoice_metadata`"""
    invoice_result = ProformaInvoiceCreateResult(**json.loads(invoice_result_json))

    SaleRecordingApplication.manager.filter(id=application_id).update(
        fakturownia_invoice_id=invoice_result.invoice_id
    )

    SaleRecordingApplication.manager.filter(id=application_id).update(
        fakturownia_invoice_number=invoice_result.invoice_number
    )

    SaleRecordingApplication.manager.filter(id=application_id).update(
        fakturownia_invoice_url=invoice_result.invoice_view_url
    )
