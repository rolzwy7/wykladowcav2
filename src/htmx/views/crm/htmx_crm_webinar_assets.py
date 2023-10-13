from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.models import WebinarAsset


def htmx_crm_delete_webinar_asset(request: HttpRequest, pk: int):
    """Delete webinar asset"""
    asset = get_object_or_404(WebinarAsset, pk=pk)
    asset.delete()
    return HttpResponse("")
