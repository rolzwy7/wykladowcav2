"""Tracking mailing"""

import re

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.cache import cache_page

from core.libs.mongo.db import MongoDBClient
from core.models import Webinar
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

    _, database = MongoDBClient.get_connection()

    click_docs = database["wykladowcav2_mailing_clicks"].find(
        # {"request_url": {"$regex": f"szkl/{webinar_id}"}}
        {"request_url": {"$regex": f"szkl/506"}}
    )

    per_campaign: dict[int, dict] = {}

    for doc in click_docs:
        campaign_id = doc["campaign_id"]

        if campaign_id in per_campaign:
            per_campaign[campaign_id]["click_count"] += 1
        else:
            per_campaign[campaign_id] = {"click_count": 1}

    # # Check cache
    # cache_key = f"CACHED-CAMPAIGN-COUNT-{campaign_id}-{pool_item_status}"
    # cache_seconds = 15  # 15 seconds
    # if cache.get(cache_key):
    #     count = cache.get(cache_key)
    #     return HttpResponse(f"{count:,}", content_type="text/plain; charset=utf8")

    # Set cache
    # cache.set(cache_key, count, timeout=cache_seconds)

    return HttpResponse(str(per_campaign), content_type="text/plain; charset=utf8")
