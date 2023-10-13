import requests
from django.conf import settings


def download_invoice(invoice_id: str) -> bytes:
    """Download invoice as PDF file"""
    response = requests.get(
        f"{settings.FAKTUROWNIA_API_URL}/invoices/{invoice_id}.pdf",
        params={"api_token": settings.FAKTUROWNIA_API_KEY},
        timeout=10,
    )

    response.raise_for_status()
    return response.content
