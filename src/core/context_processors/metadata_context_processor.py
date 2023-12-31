# flake8: noqa:E501
from django.conf import settings
from django.http import HttpRequest

COMPANY_NAME = settings.COMPANY_NAME
BASE_URL = settings.BASE_URL
APP_ENV = settings.APP_ENV


def page_title(request: HttpRequest) -> str:
    """Returns page title based on request

    Args:
        request (HttpRequest): _description_

    Returns:
        str: _description_
    """

    path = request.path

    if path == "/":  # Homepage
        return f"{COMPANY_NAME} - Strona główna"

    return COMPANY_NAME


def metadata(request: HttpRequest):
    """Metadata"""
    return {
        "META__APP_ENV": APP_ENV,
        "META__BASE_URL": BASE_URL,
        "META__TITLE": page_title(request),
        "META__DESCRIPTION": "META__DESCRIPTION",  # TODO
        "META__KEYWORDS": "META__KEYWORDS",  # TODO
        "META__HTML_LANG": "pl",
        "META__HTML_DIR": "ltr",  # direction
        "META__OG_LOCALE": "pl_PL",
        "META__OG_URL": f"{BASE_URL}{request.path}",
        "META__OG_SITE_NAME": COMPANY_NAME,
    }
