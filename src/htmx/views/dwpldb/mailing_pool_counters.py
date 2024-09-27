"""Health indicator"""

# flake8: noqa=E501

from django.core.cache import cache
from django.http import HttpResponse

from core.models.enums import MailingCampaignStatus, MailingPoolStatus
from core.models.mailing import MailingCampaign, MailingPoolManager


def mailing_pool_counters(request, campaign_status: str, pool_status: str):
    """mailing_pool_counters"""

    # Get pool status
    pool_item_status = {
        MailingPoolStatus.BEING_PROCESSED: "BEING_PROCESSED",
        MailingPoolStatus.READY_TO_SEND: "READY_TO_SEND",
        MailingPoolStatus.SENT: "SENT",
    }[pool_status]

    # Check cache
    cache_key = f"CACHED-POOL-COUNT-{campaign_status}-{pool_item_status}"
    cache_seconds = 5 * 60  # 5 minutes
    if cache.get(cache_key):
        count = cache.get(cache_key)
        return HttpResponse(str(count), content_type="text/plain; charset=utf8")

    # Get campaign ids
    camapigns_func = {
        MailingCampaignStatus.SENDING: MailingCampaign.manager.sending_status_campaigns,
        MailingCampaignStatus.PAUSED: MailingCampaign.manager.paused_status_campaigns,
        "ACTIVE": MailingCampaign.manager.active_campaigns,
    }[campaign_status]
    ids: list[int] = [_.id for _ in camapigns_func()]  # type: ignore

    # Calculate count
    mailing_manager = MailingPoolManager()
    count = mailing_manager.count_all_by_status_and_campaign_ids(pool_item_status, ids)
    mailing_manager.close()

    # Set cache
    cache.set(cache_key, count, timeout=cache_seconds)

    return HttpResponse(str(count), content_type="text/plain; charset=utf8")
