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

from core.consts import TelegramChats
from core.models import MailingPoolManager
from core.models.enums import MailingPoolStatus
from core.models.mailing import MailingPoolManager
from core.services import TelegramService


class Command(BaseCommand):
    """Mailing buckets randomize"""

    help = "Mailing buckets randomize"

    def add_arguments(self, parser): ...

    def handle(self, *args, **options):
        """handle"""

        pool_manager = MailingPoolManager()
        print("[*] Randomizing ready to send bucket ids ...")
        print(f"buckets_num={settings.MAILING_NUM_OF_PROCESSES}")
        pool_manager.randomize_buckets_ids(
            [
                MailingPoolStatus.BEING_PROCESSED,
                MailingPoolStatus.MX_VALID,
                MailingPoolStatus.READY_TO_SEND,
            ],
            buckets_num=settings.MAILING_NUM_OF_PROCESSES,
        )
        pool_manager.close()

        telegram_service = TelegramService()
        telegram_service.try_send_chat_message(
            f"Randomized buckets, MAILING_NUM_OF_PROCESSES := {settings.MAILING_NUM_OF_PROCESSES}",
            TelegramChats.OTHER,
        )
