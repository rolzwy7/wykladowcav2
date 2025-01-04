"""
Mailing sending procedure
"""

# flake8: noqa:E501
# pylint: disable=global-variable-not-assigned
# pylint: disable=broad-exception-caught
# pylint: disable=unused-variable
# pylint: disable=invalid-name

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from core.consts import TelegramChats
from core.libs.mailing.schedule import schedule_log, schedule_mailing
from core.models import MailingScheduled
from core.models.enums import MailingPoolStatus
from core.models.enums.mailing_enums import MailingScheduledStatus
from core.models.mailing import MailingPoolManager
from core.services import TelegramService


class Command(BaseCommand):
    """Mailing clean"""

    help = "Mailing schedule"

    def add_arguments(self, parser): ...

    def handle(self, *args, **options):
        """handle"""

        schedules = MailingScheduled.manager.get_ready_to_schedule()
        telegram_service = TelegramService()

        for schedule in schedules:
            print(schedule)
            # telegram_service.try_send_chat_message("", TelegramChats.OTHER)
            schedule_mailing(schedule)
