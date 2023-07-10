from django.http import HttpRequest
from django.utils.timezone import now


def dates(request: HttpRequest):
    """Dates context processor"""
    return {"CURRENT_YEAR": now().strftime("%Y")}
