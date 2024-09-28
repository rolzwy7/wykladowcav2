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
from random import randint
from smtplib import SMTPRecipientsRefused, SMTPServerDisconnected

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import F
from django.urls import reverse

from core.libs.mailing.handlers import (
    handle_any_error_occured,
    handle_complete_failure,
    handle_connection_refused_error,
    handle_daily_sending_limit_reached,
    handle_on_loop_failure,
    handle_smtp_recipients_refused_error,
    handle_smtp_server_disconnected_error,
    handle_timeout_error,
    handle_too_much_failures,
    try_to_finish_campaign,
)
from core.models import MailingCampaign, MailingPoolManager, MailingTemplate, SmtpSender
from core.models.enums import MailingPoolStatus
from core.services import SenderSmtpService
from core.services.mailing import MailingResignationService, MailingTrackingService

BASE_URL = settings.BASE_URL

MINUTE = 60
HOUR = 60 * 60


class ProcessSendingStatus:
    """Process sending status"""

    NO_EMAILS_SENT = "NO_EMAILS_SENT"
    LIMIT_REACHED = "LIMIT_REACHED"
    LIMIT_NOT_REACHED = "LIMIT_NOT_REACHED"


def process_sending(campaign_id: int, /, *, limit: int = 100) -> str:
    """Mailing sending process"""

    # Get campaign
    campaign: MailingCampaign = MailingCampaign.manager.get(id=campaign_id)
    alias = campaign.alias

    # Get template
    template: MailingTemplate = campaign.template
    html = template.html
    text = template.text

    # Get SMTP sender account + service
    smtp_sender: SmtpSender = campaign.smtp_sender
    smtp_service = SenderSmtpService(smtp_sender)

    # Open pool manager and get ready to send messages
    pool_manager = MailingPoolManager()
    documents = pool_manager.get_ready_to_send_for_campaign(campaign_id)

    # Open SMTP connection to sender
    connection = smtp_service.get_smtp_connection()
    return_value: str = ProcessSendingStatus.LIMIT_NOT_REACHED
    send_attempt_counter: int = 0
    sleep_between_each_send = 0

    for loop_idx, document in enumerate(documents):
        # Break on limit reached
        if loop_idx >= limit:
            return_value = ProcessSendingStatus.LIMIT_REACHED
            break

        # Prepare variables
        subject = campaign.get_random_subject()
        email = document["email"]
        document_id = f"{campaign_id}:{email}"
        text_content = text
        html_content = html
        any_error_occured = False

        # Prepare codes and urls
        tracking_code = MailingTrackingService.get_or_create_tracking(email)
        resignation_code = MailingResignationService.get_or_create_inactive_resignation(
            email, campaign.resignation_list
        )
        resignation_url = BASE_URL + reverse(
            "core:mailing_resignation_page_with_list",
            kwargs={
                "resignation_code": resignation_code,
                "resignation_list": campaign.resignation_list,
            },
        )

        print(f"\n[*] Processing email: {email} (resignation: {resignation_code})")

        if sleep_between_each_send:
            print(f"sleep_between_each_send: {sleep_between_each_send}")
            time.sleep(sleep_between_each_send)

        try:
            send_attempt_counter += 1
            smtp_service.send_email(
                connection=connection,
                email=email,
                alias=alias,
                subject=subject,
                html=html_content,
                text=text_content,
                resignation_url=resignation_url,
                tracking_code=tracking_code,
            )
        except TimeoutError as exception:
            handle_timeout_error(document_id, pool_manager)
            print(f"[-] TimeoutError `{email}`")
            any_error_occured = True
        except SMTPServerDisconnected as exception:
            handle_any_error_occured(campaign_id)
            handle_smtp_server_disconnected_error(
                campaign_id, document_id, pool_manager
            )
            print(f"[-] SMTPServerDisconnected `{email}`")
            any_error_occured = True
        except ConnectionRefusedError as exception:
            handle_any_error_occured(campaign_id)
            handle_connection_refused_error(campaign_id, document_id, pool_manager)
            print(f"[-] ConnectionRefusedError `{email}`")
            any_error_occured = True
        except SMTPRecipientsRefused as exception:
            handle_any_error_occured(campaign_id)
            handle_smtp_recipients_refused_error(campaign_id, document_id, pool_manager)
            print(f"[-] SMTPRecipientsRefused `{email}`")
            any_error_occured = True
        else:
            pool_manager.change_status(document_id, MailingPoolStatus.SENT)
            print(f"[+] SUCCESSFULLY sent to: `{email}`")

            # Increment daily counters
            pool_manager.inc_todays_sent_counter_for_campaign(campaign_id)
            pool_manager.inc_todays_sent_counter_for_sender(smtp_sender.username)

            # Increment sent counters
            MailingCampaign.manager.filter(id=campaign_id).update(
                stat_sent=F("stat_sent") + 1
            )

            # Increment sent so far counter if limit per day is set
            if campaign.limit_per_day != 0:
                MailingCampaign.manager.filter(id=campaign_id).update(
                    limit_sent_so_far=F("limit_sent_so_far") + 1
                )

        # Increment loop sleep if any error occured
        sleep_between_each_send = min(0.5, sleep_between_each_send + 0.01)

    pool_manager.close()  # close mongo manager

    try:
        connection.close()  # close SMTP connection
    except Exception as e:
        pass  # don't care

    if send_attempt_counter == 0:
        return_value = ProcessSendingStatus.NO_EMAILS_SENT

    return return_value


def can_process_campaing(campaign_mod_value: int, mod: int, reminder: int) -> bool:
    """can_process_campaing"""
    return campaign_mod_value % mod == reminder


class Command(BaseCommand):
    """Mailing sending command

    - Send emails from active campaigns

    """

    help = "Mailing sending"

    def add_arguments(self, parser):
        parser.add_argument("mod", type=int)
        parser.add_argument("reminder", type=int)

    def start_loop(self, mod: int, reminder: int):
        """Start infinite loop"""

        while True:
            #
            # Get all active mailing campaigns
            active_campaigns = MailingCampaign.manager.active_campaigns()

            #
            # Sleep and continue loop if no active campaigns
            if active_campaigns.count() == 0:
                print("[*] No active campaigns, sleeping 20s ...")
                time.sleep(20)
                continue

            #
            # Iterate over active campaigns and start sending process
            all_not_my_reminder = True
            for campaign in active_campaigns:
                campaign_id: int = campaign.id  # type: ignore

                if not can_process_campaing(campaign_id, mod, reminder):
                    print(
                        f"[-] NOT MY REMINDER for campaign.id:{campaign_id} % {mod} != {reminder}"
                    )
                    continue

                print("\n[*] Processing campaign:", campaign)
                all_not_my_reminder = False

                # Check if limit per day was reached:
                if campaign.is_daily_sending_limit_reached:
                    handle_daily_sending_limit_reached(campaign)
                # Check if too much failures counted
                elif (
                    campaign.pause_on_too_many_failures
                    and campaign.failure_counter >= 1_000
                ):
                    handle_too_much_failures(campaign_id, campaign.title)
                # If everything OK try to send emails batch
                else:
                    result = process_sending(campaign_id, limit=100)
                    # Try to finish campaign
                    if result == ProcessSendingStatus.NO_EMAILS_SENT:
                        print("[*] No emails sent with campaign:", campaign)
                        try_to_finish_campaign(campaign_id, campaign.title)

                    print("[*] Sleeping random 4-8s between camapings sending ...")
                    time.sleep(5 + randint(5, 10))

            # If all camapings are not my reminder wait
            if all_not_my_reminder:
                print("[*] All active campaigns are not my reminder, waiting 20s ...")
                time.sleep(20)

    def handle(self, *args, **options):
        """handle"""

        mod: int = options["mod"]
        reminder: int = options["reminder"]

        print("> Mod:", mod)
        print("> Reminder:", reminder)

        for test_idx in range(10):
            print(test_idx, can_process_campaing(test_idx, mod, reminder))

        # Infinite loop
        while True:

            # Retry loop
            retry = 0
            while retry <= 5:
                try:
                    self.start_loop(mod, reminder)
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
