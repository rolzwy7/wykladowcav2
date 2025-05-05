# flake8: noqa=E501

import requests
from django.conf import settings

from core.models import SaleRecordingApplication
from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app


@app.task(name="save_send_sale_recording_proforma", base=BaseTaskWithRetry)
def task_send_sale_recording_proforma(application_id: int):
    """Task for `send_sale_recording_proforma`"""

    application = SaleRecordingApplication.manager.get(id=application_id)
    invoice_id = application.fakturownia_invoice_id

    response = requests.request(
        "POST",
        f"{settings.FAKTUROWNIA_API_URL}/invoices/{invoice_id}/send_by_email.json?api_token={settings.FAKTUROWNIA_API_KEY}",
        timeout=15,
    )

    response.raise_for_status()
