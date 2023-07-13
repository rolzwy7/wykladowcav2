from django.conf import settings
from django.utils.timezone import now

from core.context_processors.company_context_processor import (
    company_non_request_context,
)

BASE_URL = settings.BASE_URL
INVOICE_DEADLINE_DAYS = settings.INVOICE_DEADLINE_DAYS


def get_email_common_context():
    """Get email common context"""
    return {
        "EMAIL_LOGO": f"{BASE_URL}/static/media/logos/wykladowcapl/logo.svg",
        "CURRENT_YEAR": now().strftime("%Y"),
        "INVOICE_DEADLINE_DAYS": INVOICE_DEADLINE_DAYS,
        **company_non_request_context(),
    }
