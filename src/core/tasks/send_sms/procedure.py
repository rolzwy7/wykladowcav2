from requests import Response

from core.libs.justsend.send_sms import send_sms as _send_sms


def send_sms(phone_number: str, message: str) -> Response:
    """Send SMS"""

    return _send_sms("Wykladowca", phone_number, message)
