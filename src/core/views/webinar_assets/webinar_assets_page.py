from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar, WebinarAsset, WebinarMetadata


def webinar_assets_page(request: HttpRequest, uuid: str):
    """Assets page for webinar"""
    template_name = "core/pages/asset/WebinarAssetPage.html"
    webinar_metadata = get_object_or_404(WebinarMetadata, assets_token=uuid)
    webinar: Webinar = webinar_metadata.webinar
    webinar_assets = WebinarAsset.manager.filter(webinar=webinar).order_by(
        "filename"
    )

    return TemplateResponse(
        request,
        template_name,
        {"webinar": webinar, "webinar_assets": webinar_assets},
    )


def webinar_asset_download(request: HttpRequest, uuid: str):
    """Assets download controller"""
    webinar_asset = get_object_or_404(WebinarAsset, token=uuid)
    asset_content = webinar_asset.file.read()
    content_type = webinar_asset.content_type
    response = HttpResponse(asset_content, content_type=content_type)
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{webinar_asset.filename}"'
    return response
