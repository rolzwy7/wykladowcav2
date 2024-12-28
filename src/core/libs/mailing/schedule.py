"""Schedule mailing"""

# flake8: noqa=E501

from datetime import time
from time import sleep
from typing import Optional

import requests
from django.db.models import F
from django.utils.timezone import datetime, now, timedelta
from requests.exceptions import RequestException

from core.models import MailingCampaign, MailingScheduled, MailingTemplate
from core.models.enums.mailing_enums import (
    MailingCampaignStatus,
    MailingScheduledStatus,
)


def schedule_log(schedule: MailingScheduled, log: str):
    """schedule_log"""

    timestamp = now().strftime("[%Y-%m-%d %H:%M:%S]")
    schedule_id: int = schedule.id  # type: ignore

    current_logs: str = MailingScheduled.manager.get(id=schedule_id).logi
    MailingScheduled.manager.filter(id=schedule_id).update(
        logi=f"{current_logs}{timestamp} {log}\n"
    )


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

    return True
