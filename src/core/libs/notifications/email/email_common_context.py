from django.conf import settings
from django.utils.timezone import now

from core.consts import (
    PATRON_EMAIL,
    PATRON_FIRST_NAME,
    PATRON_JOB_TITLE,
    PATRON_LAST_NAME,
    PATRON_PHONE,
)
from core.context_processors.company_context_processor import (
    company_non_request_context,
)

BASE_URL = settings.BASE_URL
INVOICE_DEADLINE_DAYS = settings.INVOICE_DEADLINE_DAYS


def get_email_common_context():
    """Get email common context"""
    return {
        "BASE_URL": BASE_URL,
        "EMAIL_LOGO": f"{BASE_URL}/static/media/logos/wykladowcapl/logo.svg",
        "CURRENT_YEAR": now().strftime("%Y"),
        "INVOICE_DEADLINE_DAYS": INVOICE_DEADLINE_DAYS,
        "PATRON_FIRST_NAME": PATRON_FIRST_NAME,
        "PATRON_LAST_NAME": PATRON_LAST_NAME,
        "PATRON_JOB_TITLE": PATRON_JOB_TITLE,
        "PATRON_EMAIL": PATRON_EMAIL,
        "PATRON_PHONE": PATRON_PHONE,
        **company_non_request_context(),
    }
