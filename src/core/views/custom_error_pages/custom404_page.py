from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import render
from django.utils.timezone import now


def custom404_page(request: HttpRequest, exception):
    """Custom 404 Not Found page"""
    return render(
        request,
        "core/404.html",
        context={
            "COMPANY_NAME": settings.COMPANY_NAME,
            "CURRENT_YEAR": now().strftime("%Y"),
        },
        status=404,
    )
