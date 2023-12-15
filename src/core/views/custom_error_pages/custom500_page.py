from django.http import HttpRequest
from django.shortcuts import render


def custom500_page(request: HttpRequest, exception=None):
    """Custom 500 Not Found page"""
    return render(request, "core/500.html", status=500)
