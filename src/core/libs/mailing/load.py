"""Load mailing e-mails"""

# flake8: noqa=E501

from random import randint

from django.conf import settings

from core.models import MailingPool
from core.models.enums import MailingPoolStatus
from core.models.mailing import MailingCampaign, MailingPoolManager


def load_emails_into_campaign(emails: list[str], mailing_campaign: MailingCampaign):
    """load_emails_into_campaign"""

    pool_manager = MailingPoolManager()
    batch = []
    mailing_campaign_id: int = mailing_campaign.id  # type: ignore
    emails_count = len(emails)

    for email in emails:

        # Decide priority
        if mailing_campaign.random_priority:
            # If random priority then priority = base + random
            priority = mailing_campaign.base_priority + randint(
                mailing_campaign.random_priority_min,
                mailing_campaign.random_priority_max,
            )
        else:
            # If not random priority then priority = base
            priority = mailing_campaign.base_priority

        # If e-mail is in comapny domain set highest priority
        if settings.COMPANY_DOMAIN in email:
            priority = 999

        # Append to pool
        batch.append(
            pool_manager.create_insert_object(
                MailingPool(
                    campaign_id=mailing_campaign_id,
                    email=email,
                    status=MailingPoolStatus.BEING_PROCESSED,
                    priority=priority,
                    bucket_id=randint(0, settings.MAILING_NUM_OF_PROCESSES - 1),
                    # bucket_id=self.mailing_campaign.smtp_sender.bucket_id,
                )
            )
        )

        # Batch insert e-mails
        if len(batch) >= 100:
            pool_manager.bulk_write_ignore_errors(batch)
            batch = []

    # Last batch insert if any left
    if batch:
        pool_manager.bulk_write_ignore_errors(batch)

    pool_manager.close()

    return emails_count
