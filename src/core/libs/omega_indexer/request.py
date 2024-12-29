"""Omega Indexer Request"""

# flake8: noqa=E501

import hashlib

import requests
from django.conf import settings


def omega_indexer_request(url: str, timeout: int = 10) -> str:
    """omega_indexer_request"""
    api_url = "https://www.omegaindexer.com/amember/dashboard/api"
    payload = {
        "apikey": settings.OMEGA_INDEXER_API_KEY,
        "campaignname": "wykladowcapl_index_"
        + hashlib.md5(url.encode()).hexdigest()[:5],
        "dripfeed": "2",
        "urls": url,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(api_url, data=payload, headers=headers, timeout=timeout)
    return response.text
