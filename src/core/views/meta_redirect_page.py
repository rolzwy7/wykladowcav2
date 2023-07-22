from django.http import HttpRequest
from django.template.response import TemplateResponse


def meta_redirect_page(request: HttpRequest):
    """Loading redirect controller"""
    webpath = request.GET.get("path", "/")
    return TemplateResponse(
        request, "core/pages/LadingRedirectPage.html", {"webpath": webpath}
    )
