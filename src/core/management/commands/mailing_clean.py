"""
Mailing sending procedure
"""

# flake8: noqa:E501
# pylint: disable=global-variable-not-assigned
# pylint: disable=broad-exception-caught
# pylint: disable=unused-variable
# pylint: disable=invalid-name

from django.core.management.base import BaseCommand

from core.consts import TelegramChats
from core.models.enums import MailingPoolStatus
from core.models.mailing import MailingPoolManager
from core.services import TelegramService


class Command(BaseCommand):
    """Mailing clean"""

    help = "Mailing clean"

    def add_arguments(self, parser): ...

    def handle(self, *args, **options):
        """handle"""

        pool_manager = MailingPoolManager()

        print("[*] Deleting processed pool items to make disk space ...")
        num_of_deleted = pool_manager.delete_not_with_statuses(
            [
                MailingPoolStatus.BEING_PROCESSED,
                MailingPoolStatus.MX_VALID,
                MailingPoolStatus.READY_TO_SEND,
            ]
        )

        telegram_service = TelegramService()
        telegram_service.try_send_chat_message(
            f"[MailingClean] Usunięto {num_of_deleted:,} przeprocesowanych dokumentów",
            TelegramChats.OTHER,
        )

        pool_manager.close()
