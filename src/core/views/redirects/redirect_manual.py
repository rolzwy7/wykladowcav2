from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from core.models import RedirectManual


def redirect_manual_endpoint(
    request: HttpRequest, slug_a: str, slug_b: str = "", slug_c: str = ""
):
    """redirect_manual_endpoint"""
    if slug_a and slug_b and slug_c:
        slug = f"/{slug_a}/{slug_b}/{slug_c}/"
    elif slug_a and slug_b:
        slug = f"/{slug_a}/{slug_b}/"
    else:
        slug = f"/{slug_a}/"

    redirect_obj = get_object_or_404(RedirectManual, slug=slug)
    status_code = int(redirect_obj.status_code)
    redirect_obj.counter = redirect_obj.counter + 1
    redirect_obj.save()

    http_redirect = HttpResponseRedirect(redirect_obj.url)
    http_redirect.status_code = status_code

    return http_redirect
