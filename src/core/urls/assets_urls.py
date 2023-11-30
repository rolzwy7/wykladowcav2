from django.urls import path

from core.views.webinar_assets import (
    webinar_asset_download,
    webinar_assets_page,
    webinar_download_assets_archive,
)

urlpatterns = [
    path(
        "pobierz/<uuid:uuid>/",
        webinar_asset_download,
        name="webinar_asset_download",
    ),
    path(
        "<uuid:uuid>/pobierz-jako-archiwum/",
        webinar_download_assets_archive,
        name="webinar_download_assets_archive",
    ),
    path(
        "<uuid:uuid>/",
        webinar_assets_page,
        name="webinar_assets_page",
    ),
]
