"""
Mailing warmup
"""

# flake8: noqa=E501

from django.core.management.base import BaseCommand

from core.consts import TelegramChats
from core.models.enums import MailingCampaignWarmupStatus
from core.models.mailing import MailingCampaign
from core.services import TelegramService


class Command(BaseCommand):
    """Mailing warmup"""

    help = "Mailing warmup"

    def add_arguments(self, parser): ...

    def handle(self, *args, **options):
        """handle"""

        telegram_service = TelegramService()
        telegram_service.try_send_chat_message(
            "Start process: Mailing warmup",
            TelegramChats.DEBUG,
        )

        warmup_campaigns = MailingCampaign.manager.filter(
            warmup_status=MailingCampaignWarmupStatus.WARMUP_ACTIVE
        )

        for warmup_campaign in warmup_campaigns:
            campaign: MailingCampaign = warmup_campaign
            campaign_id: int = campaign.id  # type: ignore

            # Save old values
            old_sleep_every_send = campaign.sleep_every_send
            old_sending_batch_size = campaign.sending_batch_size

            # Set sleep_between_batches to 1
            campaign.sleep_between_batches = 1

            # Multiply current batch size
            campaign.sending_batch_size = int(
                campaign.warmup_multiplier * campaign.sending_batch_size
            )

            # Recalculate new sleep for every send
            campaign.sleep_every_send = round(
                float((60 * 60) / campaign.sending_batch_size), 2
            )

            # If warmup max reached, finish warmup
            if campaign.sending_batch_size > campaign.warmup_max:
                campaign.warmup_status = MailingCampaignWarmupStatus.WARMUP_FINISHED
                campaign.sending_batch_size = campaign.warmup_max
                campaign.sleep_every_send = round(
                    float((60 * 60) / campaign.sending_batch_size), 2
                )
                telegram_service.try_send_chat_message(
                    "Hit warmup max",
                    TelegramChats.DEBUG,
                )

            # Save new campaign config
            campaign.save()

            notify_msg = "\n".join(
                [
                    f"WARMUP for campaign #{campaign_id} | warmup_multiplier = {campaign.warmup_multiplier}",
                    f"- sending_batch_size {old_sending_batch_size} -> {campaign.sending_batch_size}",
                    f"- sleep_every_send {old_sleep_every_send} -> {campaign.sleep_every_send}",
                ]
            )

            print(notify_msg)

            # Notify
            telegram_service.try_send_chat_message(
                notify_msg,
                TelegramChats.DEBUG,
            )
