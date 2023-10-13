# pylint: disable=abstract-method

import celery
from django.conf import settings


class BaseTaskWithRetry(celery.Task):
    """Base task"""

    autoretry_for = (Exception,)
    retry_kwargs = {"max_retries": 3 if settings.DEBUG else 10}
    retry_backoff = 5  # 5 seconds
    retry_backoff_max = 600  # 10 minutes
    retry_jitter = True
