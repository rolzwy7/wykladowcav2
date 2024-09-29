"""HTMX URLs"""

# flake8: noqa=E501

from django.urls import path

from .bisnode_2024 import bisnode_2024_download_progress
from .mailing_campaign_counters import mailing_campaign_counters
from .mailing_campaign_daily_counters import (
    mailing_daily_counters_campaign,
    mailing_daily_counters_sender,
)
from .mailing_pool_counters import mailing_pool_counters
from .queue_counts import (
    email_verify_queue_count,
    regon_queue_count,
    scraper_queue_static_count,
)

app_name = "queues"  # pylint: disable=invalid-name

urlpatterns = [
    path(
        "regon-queue-count/",
        regon_queue_count,
        name="regon-queue-count",
    ),
    path(
        "email-verify-queue-count/",
        email_verify_queue_count,
        name="email-verify-queue-count",
    ),
    path(
        "scraper-queue-static-count/",
        scraper_queue_static_count,
        name="scraper-queue-static-count",
    ),
    path(
        "bisnode-2024-download-progress/",
        bisnode_2024_download_progress,
        name="bisnode-2024-download-progress",
    ),
    path(
        "mailing-pool-counters/<str:campaign_status>/<str:pool_status>/",
        mailing_pool_counters,
        name="mailing-pool-counters",
    ),
    path(
        "mailing-campaign-counters/<int:campaign_id>/<str:pool_status>/",
        mailing_campaign_counters,
        name="mailing-campaign-counters",
    ),
    path(
        "mailing-daily-counters-campaign/<int:campaign_id>/",
        mailing_daily_counters_campaign,
        name="mailing-campaign-daily-counters-campaign",
    ),
    path(
        "mailing-daily-counters-sender/<str:sender_name>/<str:date_str>/",
        mailing_daily_counters_sender,
        name="mailing-campaign-daily-counters-sender",
    ),
]
