"""
Mailing sending procedure
"""

# flake8: noqa:E501
# pylint: disable=global-variable-not-assigned
# pylint: disable=broad-exception-caught
# pylint: disable=unused-variable
# pylint: disable=invalid-name

from django.conf import settings
from django.core.management.base import BaseCommand

from core.models.enums import MailingPoolStatus
from core.models.mailing import MailingCampaign, MailingPoolManager


class Command(BaseCommand):
    """Mailing buckets randomize"""

    help = "Mailing buckets randomize"

    def add_arguments(self, parser): ...

    def handle(self, *args, **options):
        """handle"""

        pool_manager = MailingPoolManager()
        print("[*] Randomizing ready to send bucket ids ...")
        pool_manager.randomize_buckets_ids(
            [
                MailingPoolStatus.BEING_PROCESSED,
                MailingPoolStatus.MX_VALID,
                MailingPoolStatus.READY_TO_SEND,
            ],
            buckets_num=settings.MAILING_NUM_OF_PROCESSES,
        )
        pool_manager.close()
