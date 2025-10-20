"""
Mailing processing procedure
"""

# flake8: noqa=E501
# pylint: disable=broad-exception-caught

import time
import traceback

from django.core.management.base import BaseCommand

from core.consts import TelegramChats
from core.libs.mailing.processes import process_scan_inbox
from core.models import SmtpSender
from core.services import TelegramService

SLEEP_BETWEEN_INBOX_SCANS = 10


class Command(BaseCommand):
    """Mailing scan inbox command"""

    help = "Mailing scan inbox"

    def add_arguments(self, parser): ...

    def handle(self, *args, **options):
        """handle"""

        smtp_senders = SmtpSender.manager.get_senders_for_processing()

        for smtp_sender in smtp_senders:

            print("smtp_sender:", smtp_sender)
            time.sleep(SLEEP_BETWEEN_INBOX_SCANS)

            try:
                process_scan_inbox(smtp_sender)
            except Exception as e:
                telegram_service = TelegramService()
                telegram_service.send_chat_message(
                    "\n".join(
                        [
                            f"🟥 Sender {smtp_sender}: process_scan_inbox error: {e}",
                            "\n".join(traceback.format_exc().splitlines()),
                        ]
                    ),
                    TelegramChats.DEBUG,
                )
            else:
                telegram_service = TelegramService()
                telegram_service.send_chat_message(
                    f"✅ Sender {smtp_sender}: process_scan_inbox success",
                    TelegramChats.DEBUG,
                )
            finally:
                print(f"SLEEP_BETWEEN_INBOX_SCANS: {SLEEP_BETWEEN_INBOX_SCANS}")
