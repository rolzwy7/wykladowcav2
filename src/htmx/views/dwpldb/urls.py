"""HTMX URLs"""

# flake8: noqa=E501

from django.urls import path

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
]