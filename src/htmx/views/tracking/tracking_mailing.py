"""Tracking mailing"""

from django.http import HttpResponse
from django.views.decorators.cache import cache_page

from core.services.mailing import MailingTrackingService


@cache_page(60)
def tracking_mailing(request, tracking_code: str):
    """Tracking mailing"""

    obj = MailingTrackingService.get_by_code(tracking_code)
    email = obj.email if obj else "Nie znaleziono"
    return HttpResponse(email)
