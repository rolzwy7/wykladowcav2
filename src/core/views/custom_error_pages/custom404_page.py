from django.http import HttpRequest
from django.shortcuts import render


def custom404_page(request: HttpRequest, exception):
    """Custom 404 Not Found page"""
    return render(request, "core/404.html", status=404)
