"""Schedule mailing"""

from typing import Optional

import requests
from django.utils.timezone import now
from requests.exceptions import RequestException

from core.models import MailingCampaign, MailingScheduled, MailingTemplate
from core.models.enums.mailing_enums import (
    MailingCampaignStatus,
    MailingScheduledStatus,
)
from core.models.mailing import MailingScheduled


def schedule_mailing(schedule: MailingScheduled):
    """Create mailing campaign from schedule mailing object"""

    # Mark scheduled mailing as `scheduled` to prevent re-run at any cost
    schedule.scheduled_at = now()
    schedule.status = MailingScheduledStatus.SCHEDULED
    schedule.save()

    # String timestamp
    str_ts = now().strftime("%Y%m%d")

    def fetch_html(url: str, timeout: int = 10) -> Optional[str]:
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except RequestException:
            return None

    html_content = fetch_html(schedule.url)
    if html_content:
        template = MailingTemplate(
            name=f"T_{str_ts}_{schedule.title[:25]}", html=html_content
        )
        template.save()
    else:
        raise Exception("html_content is None")

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
        allowed_to_send_after=time(5, (10 * ((day_of_week + 1) % 7)) % 60, 0, 0),
        allowed_to_send_before=time(14, 30, 0, 0),
        send_after=send_after,
    )
    campaign.save()
