"""Health indicator"""

# flake8: noqa=E501

from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from core.models.enums import MailingPoolStatus
from core.models.mailing import MailingCampaign, MailingPoolManager


def mailing_campaign_counters(request, campaign_id: int, pool_status: str):
    """mailing_campaign_counters"""

    if pool_status == "failure_counter":
        campaign = get_object_or_404(MailingCampaign, id=campaign_id)
        return HttpResponse(
            f"{campaign.failure_counter:,}", content_type="text/plain; charset=utf8"
        )

    # Get pool status
    pool_item_status = {
        MailingPoolStatus.BEING_PROCESSED: "BEING_PROCESSED",
        MailingPoolStatus.READY_TO_SEND: "READY_TO_SEND",
        MailingPoolStatus.SENT: "SENT",
    }[pool_status]

    # Check cache
    cache_key = f"CACHED-CAMPAIGN-COUNT-{campaign_id}-{pool_item_status}"
    cache_seconds = 15  # 15 seconds
    if cache.get(cache_key):
        count = cache.get(cache_key)
        return HttpResponse(f"{count:,}", content_type="text/plain; charset=utf8")

    # Calculate count
    mailing_manager = MailingPoolManager()
    count = mailing_manager.count_all_by_status_and_campaign_ids(
        pool_item_status, [campaign_id]
    )
    mailing_manager.close()

    # Set cache
    cache.set(cache_key, count, timeout=cache_seconds)

    return HttpResponse(f"{count:,}", content_type="text/plain; charset=utf8")
