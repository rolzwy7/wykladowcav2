from django.http import HttpRequest
from django.template.response import TemplateResponse


def meta_redirect_page(request: HttpRequest):
    """Loading redirect controller"""
    webpath = request.GET.get("path", "/")
    seconds = request.GET.get("seconds", "1")
    text = request.GET.get("text", "")
    return TemplateResponse(
        request,
        "core/pages/LadingRedirectPage.html",
        {"webpath": webpath, "seconds": seconds, "text": text},
    )
