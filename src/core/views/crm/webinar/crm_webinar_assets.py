"""CRM webinar assets"""

# flake8: noqa=E501

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import POST
from core.forms import WebinarAssetForm
from core.models import Webinar, WebinarAsset, WebinarMetadata
from core.services import CrmWebinarService
from core.services.webinar.crm import WebinarAssetsService


def crm_webinar_assets(request, pk: int):
    """Assets for given webinar"""
    template_name = "core/pages/crm/webinar/CrmWebinarAssets.html"
    webinar = get_object_or_404(Webinar, pk=pk)
    webinar_metadata = WebinarMetadata.objects.get(webinar=webinar)
    assets = WebinarAsset.manager.filter(webinar=webinar).order_by("filename")
    asset_service = WebinarAssetsService(webinar)
    webinar_service = CrmWebinarService(webinar)

    # Done webinars with similar name
    assets_complete = []
    if request.GET.get("autocomplete_webinar"):
        qs_autocomplete = Webinar.manager.filter(
            Q(title__icontains=request.GET["autocomplete_webinar"])
        )
    else:
        qs_autocomplete = Webinar.manager.filter(
            Q(title=webinar.title) & ~Q(id=webinar.id)
        )

    for web in qs_autocomplete:
        web_assets = WebinarAsset.manager.filter(webinar=web).order_by("filename")
        assets_complete.append((web, web_assets, web_assets.count()))

    if request.method == POST:

        if request.POST.get("autocomplete") == "on":
            ac_web_id = int(request.POST.get("autocomplete_webinar_id"))
            ac_web = Webinar.manager.get(id=ac_web_id)
            ac_web_assets: list[WebinarAsset] = WebinarAsset.manager.filter(
                webinar=ac_web
            ).order_by(
                "filename"
            )  # type: ignore
            for asset in ac_web_assets:
                WebinarAsset(
                    webinar=webinar,
                    filename=asset.filename,
                    filesize=asset.filesize,
                    content_type=asset.content_type,
                    file=asset.file,
                ).save()
            return redirect(
                reverse("core:crm_webinar_assets", kwargs={"pk": webinar.id})
            )
        else:
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
            "autocomplete_webinar": request.GET.get("autocomplete_webinar"),
            "webinar_metadata": webinar_metadata,
            "assets": assets,
            "assets_complete": assets_complete,
            **webinar_service.get_context(),
        },
    )
