from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts import POST
from core.forms import WebinarAssetForm
from core.models import Webinar, WebinarAsset
from core.services import WebinarAssetsService


def crm_webinar_assets(request, pk: int):
    """Assets for given webinar"""
    template_name = "core/pages/crm/webinar/CrmWebinarAssets.html"
    webinar = get_object_or_404(Webinar, pk=pk)
    assets = WebinarAsset.manager.filter(webinar=webinar).order_by("filename")
    service = WebinarAssetsService(webinar)

    if request.method == POST:
        form = WebinarAssetForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["file"]
            service.save_asset(file)
            return HttpResponse("OK")

    return TemplateResponse(
        request,
        template_name,
        {
            "webinar": webinar,
            "assets": assets,
        },
    )
