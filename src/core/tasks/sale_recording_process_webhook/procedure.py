# flake8: noqa=E501

import json

import requests  # pylint: disable=no-name-in-module
from django.conf import settings
from pydantic import BaseModel


class SaleRecordingProcessWebhookParams(BaseModel):
    """Params"""

    invoice_vat_id: int


def params(invoice_vat_id: int) -> str:
    """Create params"""
    json_dump = json.dumps(
        SaleRecordingProcessWebhookParams(invoice_vat_id=invoice_vat_id).dict()
    )
    return json_dump


def sale_recording_process_webhook(
    procedure_params: SaleRecordingProcessWebhookParams,
):
    """Process sale recording webhook"""

    invoice_vat_id = procedure_params.invoice_vat_id

    url = f"{settings.FAKTUROWNIA_API_URL}/invoices/{invoice_vat_id}.json"
    url += f"?api_token={settings.FAKTUROWNIA_API_KEY}"

    response = requests.get(url, timeout=15)
    response.raise_for_status()
    result_json = response.json()

    if result_json.get("from_invoice_id"):
        return int(result_json["from_invoice_id"])
    else:
        return 0
