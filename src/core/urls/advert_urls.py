from django.urls import path

from core.views.adverts import advert_popup_track_click

urlpatterns = [
    path(
        "advert-popup-redirect/<uuid:uuid>/",
        advert_popup_track_click,
        name="advert_popup_track_click",
    )
]
