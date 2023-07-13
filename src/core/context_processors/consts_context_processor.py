from django.conf import settings

from core.consts import (
    PATRON_EMAIL,
    PATRON_PHONE,
    PRICE_ADNOTATION,
    TAX_EXEMPT_TOOLTIP,
    VAT_VALUE_PERCENT,
    WE_ARE_TAX_EXEMPT,
)


def consts(request):
    """Settings context processor"""

    return {
        # Price and Tax
        "PRICE_ADNOTATION": PRICE_ADNOTATION,
        "WE_ARE_TAX_EXEMPT": WE_ARE_TAX_EXEMPT,
        "TAX_EXEMPT_TOOLTIP": TAX_EXEMPT_TOOLTIP,
        "INVOICE_DEADLINE_DAYS": settings.INVOICE_DEADLINE_DAYS,
        "VAT_VALUE_PERCENT": VAT_VALUE_PERCENT,
        # Patron
        "PATRON_EMAIL": PATRON_EMAIL,
        "PATRON_PHONE": PATRON_PHONE,
    }
