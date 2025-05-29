"""Tracking mailing"""

# flake8: noqa=E501

from django.core.cache import cache
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.cache import cache_page

from core.libs.mongo.db import MongoDBClient
from core.models.mailing import MailingCampaign
from core.services.mailing import MailingTrackingService


@cache_page(60)
def tracking_mailing(request, tracking_code: str):
    """Tracking mailing"""

    obj = MailingTrackingService.get_by_code(tracking_code)
    email = obj.email if obj else "Nie znaleziono"
    return HttpResponse(email)


def tracking_mailing_clicks(request, webinar_id: int):
    """tracking_mailing_clicks"""

    # Check cache
    cache_key = f"CACHED-TRACKING-MAILING-CLICKS-WEBINAR-{webinar_id}"
    cache_seconds = 60 * 10  # 10 minutes
    if cache.get(cache_key):
        return TemplateResponse(
            request,
            "htmx/tracking_mailing_clicks.html",
            {"per_campaign": cache.get(cache_key)},
        )

    _, database = MongoDBClient.get_connection()

    click_docs = database["wykladowcav2_mailing_clicks"].find(
        {"request_url": {"$regex": f"szkl/{webinar_id}/"}}
        # {"request_url": {"$regex": f"szkl/506"}}
    )

    per_campaign: dict[int, dict] = {}

    for doc in click_docs:
        campaign_id = doc["campaign_id"]

        if campaign_id in per_campaign:
            per_campaign[campaign_id]["click_count"] += 1
        else:
            per_campaign[campaign_id] = {
                "click_count": 1,
                "campaign": MailingCampaign.manager.filter(id=campaign_id).first(),
            }

    # Set cache
    cache.set(cache_key, per_campaign, timeout=cache_seconds)

    return TemplateResponse(
        request,
        "htmx/tracking_mailing_clicks.html",
        {"per_campaign": per_campaign},
    )
