"""Healthcheck service"""

import requests
from django.conf import settings
from requests.exceptions import HTTPError


class HealthcheckService:
    """
    Healthcheck service
    """

    def __init__(self) -> None:
        self.flower_base_url = settings.FLOWER_BASE_URL
        self.flower_user = settings.FLOWER_USER
        self.flower_password = settings.FLOWER_PASSWORD
        self.flower_timeout = 5

    def fetch_celery_workers(self):
        """Fetch all celery workers"""
        try:
            response = requests.get(
                f"{self.flower_base_url}?json=1",
                timeout=self.flower_timeout,
                auth=(self.flower_user, self.flower_password),
            )
            response.raise_for_status()
        except HTTPError:
            return []

        return response.json()["data"]

    def is_healthy(self) -> bool:
        """Check if everything is healthy"""
        celery_workers = self.fetch_celery_workers()
        return all([worker["status"] for worker in celery_workers])
