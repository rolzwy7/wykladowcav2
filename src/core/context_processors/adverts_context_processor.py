"""
Adverts context processor
"""

# flake8: noqa=E501

from django.urls import reverse

from core.models import AdvertPopup


def adverts(request):
    """Adverts context processor"""

    advert_popup = AdvertPopup.manager.get_active().first()

    if advert_popup:
        return {
            "ADVERT_POPUP": advert_popup,
            "ADVERT_POPUP_SHOW_AFTER_MS": advert_popup.show_after_seconds * 1000,
            "ADVERT_POPUP_TARGET_URL": reverse(
                "core:advert_popup_track_click", kwargs={"uuid": advert_popup.id}
            ),
        }
    else:
        return {}
