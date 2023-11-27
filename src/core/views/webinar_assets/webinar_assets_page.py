# flake8: noqa:E501
# pylint: disable=line-too-long
import io
import os
import zipfile
from pathlib import Path

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.timezone import now, timedelta

from core.models import Webinar, WebinarAsset, WebinarMetadata


def webinar_assets_page(request: HttpRequest, uuid: str):
    """Assets page for webinar"""
    template_name = "geeks/pages/webinar/WebinarAssetPage.html"
    webinar_metadata = get_object_or_404(WebinarMetadata, assets_token=uuid)
    webinar: Webinar = webinar_metadata.webinar
    webinar_assets = WebinarAsset.manager.filter(webinar=webinar).order_by("filename")

    return TemplateResponse(
        request,
        template_name,
        {
            "webinar": webinar,
            "webinar_assets": webinar_assets,
            "webinar_metadata": webinar_metadata,
            "assets_expired": now() > webinar.date + timedelta(days=21),
        },
    )


def webinar_asset_download(request: HttpRequest, uuid: str):
    """Assets download controller"""
    webinar_asset = get_object_or_404(WebinarAsset, token=uuid)
    asset_content = webinar_asset.file.read()
    content_type = webinar_asset.content_type
    response = HttpResponse(asset_content, content_type=content_type)
    response["Content-Disposition"] = f'attachment; filename="{webinar_asset.filename}"'
    return response


def webinar_download_assets_archive(request: HttpRequest, uuid: str):
    """Assets download archive controller"""
    webinar_metadata = get_object_or_404(WebinarMetadata, assets_token=uuid)
    webinar: Webinar = webinar_metadata.webinar
    webinar_assets = WebinarAsset.manager.filter(webinar=webinar).order_by("filename")

    # Create a BytesIO buffer to store the ZIP file.
    buffer = io.BytesIO()

    # media/uploads/webinar_assets

    # Create a ZIP file.
    with zipfile.ZipFile(buffer, "w") as zip_file:
        # Loop through each file and add it to the ZIP file.
        for asset in webinar_assets:
            filepath = Path(settings.MEDIA_ROOT, str(asset.file))
            if filepath.is_file():
                zip_file.write(filepath, os.path.basename(filepath))

    # Seek to the beginning of the buffer.
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/zip")
    filename = "Materialy_szkoleniowe.zip"
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response
