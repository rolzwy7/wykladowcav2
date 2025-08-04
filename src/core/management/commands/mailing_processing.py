"""
Mailing processing procedure
"""

# flake8: noqa=E501
# pylint: disable=broad-exception-caught

import logging
import time
import traceback

from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta

from core.consts import TelegramChats
from core.libs.mailing.handlers import handle_complete_failure, handle_on_loop_failure
from core.libs.mailing.processes import (
    process_blacklist,
    process_bounces,
    process_check_mx,
    process_load_cache,
    process_scan_inbox,
)
from core.models import MailingBounceManager, MailingPoolManager, SmtpSender
from core.models.mailing import MailingCampaign
from core.services import TelegramService

logging.getLogger("flufl.bounce").setLevel(logging.WARNING)


INBOX_SCAN_CACHE = {}

SLEEP_BETWEEN_LOOPS_SECONDS = 10
SLEEP_ON_NO_ACTIVE_CAMPAIGNS = 120

MINUTE = 60
HOUR = 60 * 60


class Command(BaseCommand):
    """Mailing processing command"""

    help = "Mailing processing"

    def add_arguments(self, parser):
        parser.add_argument(
            "--scan-inbox", action="store_true", help="Scan inboxes and exit"
        )

    def start_loop(self, cache: dict):
        """Start infinite loop"""
        next_inbox_scan_at = now() - timedelta(days=999)

        while True:

            #
            # Run inboxes scan every hour
            # if now() > next_inbox_scan_at:
            #     next_inbox_scan_at = now() + timedelta(hours=1)
            #     for sender in SmtpSender.objects.all():  # pylint: disable=no-member
            #         if sender.exclude_from_processing:
            #             print(f"Skipping sender {sender} from processing (inbox scan)")
            #             continue
            #         process_scan_inbox(sender, cache)
            #

            # Get active campaigns
            active_campaigns = MailingCampaign.manager.active_campaigns_for_processing()
            active_campaigns_ids = []
            if active_campaigns.count():
                active_campaigns_ids = [_.id for _ in active_campaigns]  # type: ignore
                print("[*] Active campaigns IDs", active_campaigns_ids)
            else:
                print(
                    f"[-] No active campaigns left, waiting {SLEEP_ON_NO_ACTIVE_CAMPAIGNS}s"
                )
                time.sleep(SLEEP_ON_NO_ACTIVE_CAMPAIGNS)
                continue
            #
            # Open managers
            pool_manager = MailingPoolManager()
            bounce_manager = MailingBounceManager()
            #
            # Run at every loop
            for active_id in active_campaigns_ids:
                process_check_mx(pool_manager, [active_id], process_count=200)
                # process_bounces(
                #     pool_manager, bounce_manager, [active_id], process_count=200
                # )
                process_blacklist(pool_manager, [active_id], process_count=200)
            #
            # Close managers
            pool_manager.close()
            bounce_manager.close()
            #
            # Sleep between loops
            print(f"[*] Waiting {SLEEP_BETWEEN_LOOPS_SECONDS} seconds ...")
            time.sleep(SLEEP_BETWEEN_LOOPS_SECONDS)

    def main(self, cache: dict):
        """main"""

        # Infinite loop
        while True:
            # Retry loop
            retry = 0
            while retry <= 5:
                try:
                    # Start infinite loop
                    self.start_loop(cache)
                except Exception as e:
                    retry += 1
                    handle_on_loop_failure(
                        retry,
                        str(e),
                        "\n".join(traceback.format_exc().splitlines()),
                        "mailing_processing.py",
                    )
                else:
                    retry = 0

            # Complete failure occurs here
            handle_complete_failure("MAILING PROCESSING KOMPLETNIE SIĘ WYJEBAŁ")

    def handle(self, *args, **options):
        """handle"""

        # Load cache once at the start of program
        cache = process_load_cache()
        print(f"\n[*] Cache has {len(INBOX_SCAN_CACHE):,} elements")

        if options["scan_inbox"]:
            for sender in SmtpSender.objects.all():  # pylint: disable=no-member
                time.sleep(2)
                if sender.exclude_from_processing:
                    print(f"Skipping sender {sender} from processing (inbox scan)")
                    continue
                try:
                    process_scan_inbox(sender, cache)
                except Exception as e:
                    telegram_service = TelegramService()
                    telegram_service.send_chat_message(
                        f"🟥 Sender {sender}: process_scan_inbox error: {e}",
                        TelegramChats.OTHER,
                    )
                else:
                    telegram_service = TelegramService()
                    telegram_service.send_chat_message(
                        f"✅ Sender {sender}: process_scan_inbox success",
                        TelegramChats.OTHER,
                    )

            exit(0)

        # Execute main
        self.main(cache)
