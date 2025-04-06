"""Send SMS"""

# flake8: noqa=E501

import requests
from django.conf import settings


def send_sms(
    from_sender: str,
    phone_number: str,
    message: str,
    bulk_variant: str = "PRO",
    double_encode: bool = False,
    timeout: int = 10,
):
    """Send SMS message"""
    url = f"{settings.JUST_SEND_API_URL}/message/send"
    headers = {
        "App-Key": settings.JUST_SEND_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "message": message,
        "from": from_sender,
        "bulkVariant": bulk_variant,
        "doubleEncode": double_encode,
        "to": phone_number,
    }
    response = requests.post(url, json=payload, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.json()
