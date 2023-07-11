from django.urls import path

from core.views.webinar_assets import (
    webinar_asset_download,
    webinar_assets_page,
)

urlpatterns = [
    path(
        "pobierz/<uuid:uuid>/",
        webinar_asset_download,
        name="webinar_asset_download",
    ),
    path(
        "<uuid:uuid>/",
        webinar_assets_page,
        name="webinar_assets_page",
    ),
]
