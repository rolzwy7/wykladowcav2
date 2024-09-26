"""Mailing handlers"""

# flake8: noqa

import time

from django.db.models import F

from core.consts import TelegramChats
from core.models import MailingCampaign, MailingPoolManager
from core.models.enums import MailingCampaignStatus, MailingPoolStatus
from core.services import TelegramService


def handle_daily_sending_limit_reached(campaign: MailingCampaign):
    """Handle daily sending limit reached event"""
    telegram_service = TelegramService()

    telegram_service.try_send_chat_message(
        f"Kampania mailingowa {campaign.title}: osiągnięto limit dzienny ({campaign.limit_per_day}/{campaign.limit_sent_so_far}) dla tej kampanii",
        TelegramChats.OTHER,
    )

    campaign.status = MailingCampaignStatus.PAUSED
    campaign.limit_sent_so_far = 0
    campaign.save()


def try_to_finish_campaign(campaign_id: int, campaign_title: str):
    """Try to finish campaign if there are no init-like emails left"""
    pool_manager = MailingPoolManager()
    campaign_is_finished = pool_manager.is_campaign_finished(campaign_id)
    if campaign_is_finished:
        print("[*] No init emails left, closing campaign:", campaign_id)

        MailingCampaign.manager.filter(id=campaign_id).update(
            status=MailingCampaignStatus.DONE
        )

        telegram_service = TelegramService()
        telegram_service.try_send_chat_message(
            f"Kampania mailingowa zakończona: {campaign_title}",
            TelegramChats.OTHER,
        )

    pool_manager.close()


def handle_timeout_error(document_id: str, pool_manager: MailingPoolManager):
    """Handle timeout error"""
    pool_manager.change_status(document_id, MailingPoolStatus.BEING_PROCESSED)
    print("[*] Sleeping after timeout 30s ...")
    time.sleep(30)


def handle_smtp_server_disconnected_error(
    campaign_id: int, document_id: str, pool_manager: MailingPoolManager
):
    """Handle smtp server disconnected error"""
    pool_manager.change_status(document_id, MailingPoolStatus.SMTP_SERVER_DISCONNECTED)
    MailingCampaign.manager.filter(id=campaign_id).update(smtp_server_disconnected=True)


def handle_smtp_recipients_refused_error(
    campaign_id: int, document_id: str, pool_manager: MailingPoolManager
):
    """Handle smtp recipients refused error"""
    pool_manager.change_status(document_id, MailingPoolStatus.RECIPIENT_REFUSED)
    MailingCampaign.manager.filter(id=campaign_id).update(smtp_recipients_refused=True)


def handle_connection_refused_error(
    campaign_id: int, document_id: str, pool_manager: MailingPoolManager
):
    """Handle connection refused error"""
    pool_manager.change_status(document_id, MailingPoolStatus.CONNECTION_REFUSED)
    MailingCampaign.manager.filter(id=campaign_id).update(connection_refused=True)


def handle_any_error_occured(campaign_id: int):
    """Handle any error occured event"""
    MailingCampaign.manager.filter(id=campaign_id).update(
        any_error_occured=True, failure_counter=F("failure_counter") + 1
    )


def handle_too_much_failures(campaign_id: int, campaign_title: str):
    """Handle too much failures event"""
    MailingCampaign.manager.filter(id=campaign_id).update(
        status=MailingCampaignStatus.PAUSED
    )

    telegram_service = TelegramService()
    telegram_service.try_send_chat_message(
        f"Zbyt dużo błędów: {campaign_title}",
        TelegramChats.OTHER,
    )


def handle_on_loop_failure(
    retry: int, exception_str: str, traceback_str: str, program_name: str
):
    """handle_on_processing_loop_failure"""
    telegram_service = TelegramService()
    telegram_service.send_chat_message(
        f"{program_name} retry={retry}, {exception_str}:\n{traceback_str}",
        TelegramChats.OTHER,
    )
    wait_time_seconds = (retry + 1) * (1 * 60)
    print(f"[*] Waiting after failure: {wait_time_seconds}")
    time.sleep(wait_time_seconds)


def handle_complete_failure(message: str):
    """handle_complete_failure"""
    telegram_service = TelegramService()
    telegram_service.send_chat_message(
        message,
        TelegramChats.OTHER,
    )
    print("[*] Sleeping 8 hours on complete failure")
    time.sleep(8 * (60 * 60))
