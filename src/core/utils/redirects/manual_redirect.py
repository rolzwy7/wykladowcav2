"""
Manual redirect handler
"""
# flake8: noqa=E501
from typing import Optional

from django.db.models import F
from django.http import HttpResponseRedirect

from core.models import RedirectManual


def manual_redirect(slug: str) -> Optional[HttpResponseRedirect]:
    """Check if manual redirect exists and if it does, return it

    Additionaly increase redirect counter by 1
    """
    try:
        redirect_obj = RedirectManual.manager.get(slug=slug)
    except RedirectManual.DoesNotExist:  # pylint: disable=no-member
        return None
    else:
        status_code = int(redirect_obj.status_code)

        # Prepare redirect response
        http_redirect = HttpResponseRedirect(redirect_obj.url)
        http_redirect.status_code = status_code

        # increment redirect coutner by 1
        RedirectManual.manager.filter(slug=slug).update(counter=F("counter") + 1)

        return http_redirect
