# flake8: noqa:E501
from django.http import HttpRequest


def links(request: HttpRequest):
    """Links context processor"""
    return {
        "LINK_KADRY_PLACE_GRUPA_WSPARCIA": "https://www.facebook.com/groups/KadryPlaceGrupaWsparcia/",
        "LINK_KSIEGOWOSC_KADRY_DAM_PRACE": "https://www.facebook.com/groups/pracawkadrachiksiegowosci/",
    }
