from core.consts import TAX_EXEMPT_TOOLTIP, WE_ARE_TAX_EXEMPT


def settings(request):
    """Adds given settings into global context"""

    return {
        "WE_ARE_TAX_EXEMPT": WE_ARE_TAX_EXEMPT,
        "TAX_EXEMPT_TOOLTIP": TAX_EXEMPT_TOOLTIP,
    }
