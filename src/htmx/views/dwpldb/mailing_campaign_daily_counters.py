"""Health indicator"""

# flake8: noqa=E501

from django.core.cache import cache
from django.http import HttpResponse

from core.models.mailing import MailingPoolManager


def mailing_daily_counters_campaign(request, campaign_id: int):
    """mailing_daily_counters_campaign"""

    cache_key = f"CACHED-CAMPAIGN-DAILY-COUNTER-{campaign_id}"
    cache_seconds = 15 * 60  # 15 minutes
    if cache.get(cache_key):
        count = cache.get(cache_key)
        return HttpResponse(f"{count:,}", content_type="text/plain; charset=utf8")
    else:
        mailing_manager = MailingPoolManager()
        document = mailing_manager.get_sent_counter_for_campaign(campaign_id)

        if document:
            count = document["counter"]
            cache.set(cache_key, count, timeout=cache_seconds)
            return HttpResponse(f"{count:,}", content_type="text/plain; charset=utf8")
        else:
            return HttpResponse("not_found", content_type="text/plain; charset=utf8")


def mailing_daily_counters_sender(request, sender_name: str, date_str: str):
    """mailing_daily_counters_sender"""

    mailing_manager = MailingPoolManager()

    document = mailing_manager.get_todays_sent_counter_for_sender(
        sender_name, date_str=date_str
    )

    if document:
        return HttpResponse(
            f"{document['counter']:,}", content_type="text/plain; charset=utf8"
        )
    else:
        return HttpResponse("not_found", content_type="text/plain; charset=utf8")
