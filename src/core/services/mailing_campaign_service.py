from django.core.files.uploadedfile import InMemoryUploadedFile

from core.models import MailingCampaign, MailingPool, MailingPoolManager
from core.models.enums import MailingPoolStatus, mailing_pool_status_display_map


class MailingCampaignService:
    """Mailing campaign service"""

    def __init__(self, mailing_campaign: MailingCampaign) -> None:
        self.mailing_campaign = mailing_campaign

    def get_email_count_for_campaign(self, campaign_id: int) -> int:
        """Get count of all emails that are in given campaign"""
        return MailingPoolManager().get_email_count_for_campaign(campaign_id)

    def group_by_count_statuses(self, campaign_id: int):
        """Perform group-by-count operation on statuses"""
        ret = [
            (
                mailing_pool_status_display_map.get(document["_id"], "???"),
                document["count"],
            )
            for document in MailingPoolManager().group_by_count_statuses(
                campaign_id
            )
        ]

        return sorted(ret, key=lambda x: x[1])

    def delete_all_emails(self) -> None:
        """Delete all emails from campaign"""
        mailing_campaign_id: int = self.mailing_campaign.id  # type: ignore
        pool_manager = MailingPoolManager()
        pool_manager.database.wykladowcav2_mailing_pool.delete_many(
            {"campaign_id": mailing_campaign_id}
        )

    def load_emails_from_file_into_campaign(
        self, file: InMemoryUploadedFile
    ) -> None:
        """Load emails from file into campaign"""

        pool_manager = MailingPoolManager()
        batch = []

        for line in file:
            if isinstance(line, str):
                email = line.strip().lower()
            else:
                email = str(line, "utf8").strip().lower()

            mailing_campaign_id: int = self.mailing_campaign.id  # type: ignore

            batch.append(
                pool_manager.create_upsert_object(
                    MailingPool(
                        campaign_id=mailing_campaign_id,
                        email=email,
                        status=MailingPoolStatus.BEING_PROCESSED,
                        priority=100,
                    )
                )
            )

            if len(batch) >= 100:
                pool_manager.database.wykladowcav2_mailing_pool.bulk_write(
                    batch
                )
                batch = []

        if batch:
            pool_manager.database.wykladowcav2_mailing_pool.bulk_write(batch)

        pool_manager.close()
