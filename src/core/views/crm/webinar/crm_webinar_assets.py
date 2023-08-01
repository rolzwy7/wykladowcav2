from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts import POST
from core.forms import WebinarAssetForm
from core.models import Webinar, WebinarAsset, WebinarMetadata
from core.services import CrmWebinarService, WebinarAssetsService


def crm_webinar_assets(request, pk: int):
    """Assets for given webinar"""
    template_name = "core/pages/crm/webinar/CrmWebinarAssets.html"
    webinar = get_object_or_404(Webinar, pk=pk)
    webinar_metadata = WebinarMetadata.objects.get(webinar=webinar)
    assets = WebinarAsset.manager.filter(webinar=webinar).order_by("filename")
    asset_service = WebinarAssetsService(webinar)
    webinar_service = CrmWebinarService(webinar)

    if request.method == POST:
        form = WebinarAssetForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["file"]
            asset_service.save_asset(file)
            return HttpResponse("OK")

    return TemplateResponse(
        request,
        template_name,
        {
            "webinar": webinar,
            "webinar_metadata": webinar_metadata,
            "assets": assets,
            **webinar_service.get_context(),
        },
    )
