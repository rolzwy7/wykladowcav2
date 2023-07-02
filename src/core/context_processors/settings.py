from core.consts import PRICE_ADNOTATION, TAX_EXEMPT_TOOLTIP, WE_ARE_TAX_EXEMPT


def settings(request):
    """Adds given settings into global context"""

    return {
        "PRICE_ADNOTATION": PRICE_ADNOTATION,
        "WE_ARE_TAX_EXEMPT": WE_ARE_TAX_EXEMPT,
        "TAX_EXEMPT_TOOLTIP": TAX_EXEMPT_TOOLTIP,
    }
