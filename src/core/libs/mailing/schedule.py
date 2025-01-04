"""Schedule mailing"""

# flake8: noqa=E501

from datetime import time
from time import sleep
from typing import Optional

import requests
from django.conf import settings
from django.utils.timezone import datetime, now, timedelta
from requests.exceptions import RequestException

from core.models import MailingCampaign, MailingScheduled, MailingTemplate
from core.models.enums.mailing_enums import (
    MailingCampaignStatus,
    MailingScheduledStatus,
)

from .export import (
    export_emails_campaign_clicks,
    export_emails_lecturer_all_webinars,
    export_emails_lecturer_done_webinars,
    export_emails_lecturer_participants_free,
    export_emails_mongo_tagged,
)
from .load import load_emails_into_campaign
from .test_email import send_campaign_test_email


def schedule_log(schedule: MailingScheduled, log: str):
    """schedule_log"""

    timestamp = now().strftime("[%Y-%m-%d %H:%M:%S]")
    schedule_id: int = schedule.id  # type: ignore

    current_logs: str = MailingScheduled.manager.get(id=schedule_id).logi
    _log = f"{current_logs}{timestamp} {log}"
    print(_log)
    MailingScheduled.manager.filter(id=schedule_id).update(logi=f"{_log}\n")


def schedule_mailing(schedule: MailingScheduled) -> bool:
    """Create mailing campaign from schedule mailing object"""

    schedule_id: int = schedule.id  # type: ignore

    # Mark scheduled mailing as `scheduled` to prevent re-run at any cost
    MailingScheduled.manager.filter(id=schedule_id).update(
        status=MailingScheduledStatus.SCHEDULED
    )
    schedule_log(schedule, "Marked Schedule as `SCHEDULED`")

    # String timestamp
    str_ts = now().strftime("%Y%m%d")

    # URL fetching function
    def fetch_html(url: str, timeout: int = 10) -> Optional[str]:
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except RequestException:
            return None

    # Try to fetch HTML from URL
    for idx in range(3):
        html_content = fetch_html(schedule.url)
        if html_content:
            schedule_log(schedule, "Fetched URL successfully")
            break
        else:
            wait_value_s = (idx + 1) * 15
            schedule_log(
                schedule, f"Failed to fetch URL, try {idx+1}, wait {wait_value_s}s"
            )
            sleep(wait_value_s)

    # Create template of return with failure
    if html_content:
        schedule_log(schedule, "Creating template from fetched URL")
        template = MailingTemplate(
            name=f"T_{str_ts}_{schedule.title[:25]}", html=html_content
        )
        template.save()
    else:
        schedule_log(schedule, "Failed to fetch URL on all retries")
        return False

    # Determine the base date
    target_date = schedule.target_date
    base_date = datetime.combine(target_date, time(10, 0, 0, 0))
    base_date = base_date.astimezone(now().tzinfo)

    # Create datetimes for mailing campaign
    day_of_week = now().weekday()
    schedule_log(schedule, f"day_of_week: {day_of_week}")

    send_after = base_date.replace(hour=3)
    schedule_log(schedule, f"send_after: {send_after}")

    allowed_to_send_after = base_date.replace(hour=7, minute=30)
    allowed_to_send_after += timedelta(minutes=((day_of_week + 1) % 7) * 10)
    schedule_log(schedule, f"allowed_to_send_after: {allowed_to_send_after}")

    allowed_to_send_before = base_date.replace(hour=16, minute=0)
    schedule_log(schedule, f"allowed_to_send_before: {allowed_to_send_before}")

    campaign = MailingCampaign(
        webinar=schedule.webinar,
        title=schedule.title,
        smtp_sender=schedule.smtp_sender,
        subjects=schedule.subjects,
        target_code=schedule.target_code,
        alias=schedule.alias,
        template=template,
        resignation_list=schedule.resignation_list,
        status=MailingCampaignStatus.SENDING,
        allowed_to_send_after=allowed_to_send_after,
        allowed_to_send_before=allowed_to_send_before,
        send_after=send_after,
    )
    campaign.save()

    campaign_id: int = campaign.id  # type: ignore # pylint: disable=no-member
    schedule_log(schedule, f"Created mailing camapign ID={campaign_id}")

    # Set created campaign
    MailingScheduled.manager.filter(id=schedule_id).update(campaign_id=campaign)

    # Set `scheduled_at` time
    MailingScheduled.manager.filter(id=schedule_id).update(scheduled_at=now())

    # Insert tagged e-mails from mongo
    for tag in schedule.tags.split("\n"):

        # CAMPAIGN_CLICKS:<campaign_id:int>
        if tag.startswith("CAMPAIGN_CLICKS:"):
            param_campaign_id = int(tag.split(":")[1])
            emails_count = load_emails_into_campaign(
                export_emails_campaign_clicks(param_campaign_id), campaign
            )
            schedule_log(schedule, f"CAMPAIGN_CLICKS emails_count={emails_count}")

        # LECTURER_PARTICIPANTS_FREE:<lecturer_id:int>
        elif tag.startswith("LECTURER_PARTICIPANTS_FREE:"):
            param_lecturer_id = int(tag.split(":")[1])
            emails_count = load_emails_into_campaign(
                export_emails_lecturer_participants_free(param_lecturer_id), campaign
            )
            schedule_log(
                schedule, f"LECTURER_PARTICIPANTS_FREE emails_count={emails_count}"
            )

        # LECTURER_PARTICIPANTS_DONE_WEBINARS:<lecturer_id:int>
        elif tag.startswith("LECTURER_PARTICIPANTS_DONE_WEBINARS:"):
            param_lecturer_id = int(tag.split(":")[1])
            emails_count = load_emails_into_campaign(
                export_emails_lecturer_done_webinars(param_lecturer_id), campaign
            )
            schedule_log(
                schedule,
                f"LECTURER_PARTICIPANTS_DONE_WEBINARS emails_count={emails_count}",
            )

        # LECTURER_PARTICIPANTS_ALL_WEBINARS:<lecturer_id:int>
        elif tag.startswith("LECTURER_PARTICIPANTS_ALL_WEBINARS:"):
            param_lecturer_id = int(tag.split(":")[1])
            emails_count = load_emails_into_campaign(
                export_emails_lecturer_all_webinars(param_lecturer_id), campaign
            )
            schedule_log(
                schedule,
                f"LECTURER_PARTICIPANTS_ALL_WEBINARS emails_count={emails_count}",
            )

        # LOAD FROM MONGO
        else:
            emails_count = load_emails_into_campaign(
                export_emails_mongo_tagged(tag), campaign
            )
            schedule_log(schedule, f"MONGO_TAG tag={tag} emails_count={emails_count}")

    # Test send
    send_campaign_test_email(settings.COMPANY_OFFICE_EMAIL, campaign)

    return True
