"""
Mailing sending procedure
"""

# flake8: noqa:E501
# pylint: disable=global-variable-not-assigned
# pylint: disable=broad-exception-caught
# pylint: disable=unused-variable
# pylint: disable=invalid-name

import time
import traceback

from django.conf import settings
from django.core.management.base import BaseCommand

from core.libs.mailing.handlers import (
    handle_complete_failure,
    handle_daily_sending_limit_reached,
    handle_on_loop_failure,
    handle_too_much_failures,
    try_to_finish_campaign,
)
from core.libs.mailing.sending import process_sending
from core.models import MailingCampaign
from core.models.mailing.mailing_duplicate_sends import MailingDuplicateSendsManager
from core.models.mailing.mailing_pool_model import MailingPoolManager

BASE_URL = settings.BASE_URL

MINUTE = 60
HOUR = 60 * 60


class Command(BaseCommand):
    """Mailing sending command

    - Send emails from active campaigns

    """

    help = "Mailing sending"

    def add_arguments(self, parser):
        parser.add_argument("bucket_id", type=int)
        parser.add_argument("--sender", type=str)

    def start_loop(
        self,
        pool_manager: MailingPoolManager,
        duplicates_manager: MailingDuplicateSendsManager,
        bucket_id: int,
    ):
        """Start infinite loop"""

        # Get all active mailing campaigns
        active_campaigns = MailingCampaign.manager.active_campaigns_random_order()

        # Sleep and continue loop if no active campaigns
        if active_campaigns.count() == 0:
            print("[*] No active campaigns for sending, sleeping 120s ...")
            time.sleep(120)
            return

        # Iterate over active campaigns and start sending process
        print(
            "[*] Active campaigns (random order):",
            [_.id for _ in active_campaigns],  # type: ignore
        )

        sleep_after_campaign_loop = 15

        for campaign in active_campaigns:
            campaign_id: int = campaign.id  # type: ignore
            print(f"\n[*] Campaign (ID={campaign_id})", campaign.title)
            print("Bucket_id :=", bucket_id)

            # If first bucket try to finish this campaign
            if bucket_id == 0:
                print("[bucket 0 op] Trying to finish this campaign")
                if try_to_finish_campaign(pool_manager, campaign_id, campaign.title):
                    continue

            # Check if limit per day was reached:
            if campaign.is_daily_sending_limit_reached:
                print("[*] Daily limit reached")
                handle_daily_sending_limit_reached(campaign)
            # Check if too much failures counted
            elif (
                campaign.pause_on_too_many_failures
                and campaign.failure_counter >= 1_000
            ):
                handle_too_much_failures(campaign_id, campaign.title)
            # If everything OK try to send emails batch
            else:
                result = process_sending(
                    pool_manager,
                    duplicates_manager,
                    campaign_id,
                    bucket_id,
                    limit=campaign.sending_batch_size,
                )
                if result == "no_items_in_pool_for_given_bucket":
                    print("[*] Skipping wait: campaign.sleep_between_batches")
                    continue
                else:
                    sleep_after_campaign_loop = 0
                    time.sleep(campaign.sleep_between_batches)

        time.sleep(sleep_after_campaign_loop)

    def handle(self, *args, **options):
        """handle"""

        bucket_id: int = options["bucket_id"]

        print("> Bucket ID:", bucket_id)

        # Infinite loop
        while True:

            # Retry loop
            retry = 0
            while retry <= 5:
                pool_manager = MailingPoolManager()
                duplicates_manager = MailingDuplicateSendsManager()
                try:
                    while True:
                        self.start_loop(pool_manager, duplicates_manager, bucket_id)
                except Exception as e:
                    retry += 1
                    handle_on_loop_failure(
                        retry,
                        str(e),
                        "\n".join(traceback.format_exc().splitlines()),
                        "mailing_sending.py",
                    )
                else:
                    retry = 0

            # When something went completely wrong send telegram message
            handle_complete_failure("MAILING SENDING KOMPLETNIE SIĘ WYJEBAŁ")
