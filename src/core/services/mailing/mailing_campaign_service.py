"""Mailing Campaign Service"""

# flake8: noqa=E501

from datetime import time

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.timezone import now, timedelta

from core.libs.mailing.load import load_emails_into_campaign
from core.models import MailingCampaign, MailingPoolManager
from core.models.enums import (
    MailingCampaignStatus,
    MailingPoolStatus,
    mailing_pool_status_display_map,
)


class MailingCampaignService:
    """Mailing campaign service"""

    def __init__(self, mailing_campaign: MailingCampaign) -> None:
        self.mailing_campaign = mailing_campaign

    def get_email_count_for_campaign(self, campaign_id: int) -> int:
        """Get count of all emails that are in given campaign"""
        return MailingPoolManager().get_email_count_for_campaign(campaign_id)

    def get_spam_phrases(self):
        """Get spam phrases"""
        ret = []
        if self.mailing_campaign.template:
            template_text = self.mailing_campaign.template.text
            spam_phrases = ["credit", "kredyt", "free", "tax", "life"]
            for spam_phrase in spam_phrases:
                if spam_phrase in template_text.lower():
                    ret.append(spam_phrase)

        return ret

    def group_by_count_statuses(self, campaign_id: int):
        """Perform group-by-count operation on statuses"""
        pool_manager = MailingPoolManager()
        ret = [
            (
                document["_id"],
                mailing_pool_status_display_map.get(document["_id"], "???"),
                document["count"],
            )
            for document in pool_manager.group_by_count_statuses(campaign_id)
        ]
        pool_manager.close()

        return sorted(ret, key=lambda x: x[2], reverse=True)

    def delete_all_emails(self) -> None:
        """Delete all emails from campaign"""
        mailing_campaign_id: int = self.mailing_campaign.id  # type: ignore
        pool_manager = MailingPoolManager()
        pool_manager.collection.delete_many({"campaign_id": mailing_campaign_id})
        pool_manager.close()

    def reset_campaign(self) -> None:
        """Reset campaign"""
        mailing_campaign_id: int = self.mailing_campaign.id  # type: ignore
        pool_manager = MailingPoolManager()
        pool_manager.collection.update_many(
            {
                "campaign_id": mailing_campaign_id,
                "status": {"$ne": MailingPoolStatus.SENT},
            },
            {"$set": {"status": MailingPoolStatus.BEING_PROCESSED}},
        )
        pool_manager.close()

        # Start sending tomorrow as 02:00
        send_after = now()
        send_after = send_after + timedelta(days=1)
        send_after = send_after.replace(hour=2, minute=0, second=0)

        self.mailing_campaign.status = MailingCampaignStatus.SENDING
        self.mailing_campaign.allowed_to_send_after = time(4, 0, 0, 0)
        self.mailing_campaign.allowed_to_send_before = time(13, 30, 0, 0)
        self.mailing_campaign.send_after = send_after

        self.mailing_campaign.resets_counter = self.mailing_campaign.resets_counter + 1
        self.mailing_campaign.failure_counter = 0

        self.mailing_campaign.any_error_occured = False
        self.mailing_campaign.smtp_server_disconnected = False
        self.mailing_campaign.connection_refused = False
        self.mailing_campaign.smtp_recipients_refused = False
        self.mailing_campaign.save()

    def load_emails_from_file_into_campaign(self, file: InMemoryUploadedFile) -> None:
        """Load emails from file into campaign"""

        emails: list[str] = []
        for line in file:
            email = (
                line.strip().lower()
                if isinstance(line, str)
                else str(line, "utf8").strip().lower()
            )
            emails.append(email)

        load_emails_into_campaign(emails, self.mailing_campaign)
