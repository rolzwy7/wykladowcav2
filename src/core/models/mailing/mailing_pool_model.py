from django.conf import settings
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from pymongo import UpdateOne

from core.libs.mongo.db import get_mongo_connection
from core.models.enums import MailingPoolStatus


class MailingPool(BaseModel):
    """Represents email bounce"""

    campaign_id: int
    email: str
    status: str
    priority: int


class MailingPoolManager:
    """Mailing pool manager"""

    def __init__(self) -> None:
        client, database = get_mongo_connection()
        self.client = client
        self.database = database

        if settings.APP_ENV == "production":
            self.collection = self.database.wykladowcav2_mailing_pool
        elif settings.APP_ENV == "staging":
            self.collection = self.database.wykladowcav2_mailing_pool_staging
        else:
            self.collection = self.database.wykladowcav2_mailing_pool_dev

    def close(self):
        """Close connection"""
        self.client.close()

    def create_upsert_object(self, pool_object: MailingPool) -> UpdateOne:
        """Upsert pool object into collection"""
        new_id = f"{pool_object.campaign_id}:{pool_object.email}"
        return UpdateOne(
            {"_id": new_id},
            {"$set": {"_id": new_id, **pool_object.dict()}},
            upsert=True,
        )

    def get_email_count_for_campaign(self, campaign_id: int) -> int:
        """Get count of all emails that are in given campaign"""
        return self.collection.count_documents({"campaign_id": campaign_id})

    def group_by_count_statuses(self, campaign_id: int):
        """Perform group-by-count operation on statuses"""
        return self.collection.aggregate(
            [
                {"$match": {"campaign_id": campaign_id}},
                {"$group": {"_id": "$status", "count": {"$sum": 1}}},
            ]
        )

    def change_status(self, document_id: str, status: str) -> None:
        """Change status of pool object"""
        self.collection.update_one(
            {"_id": document_id}, {"$set": {"status": status}}
        )

    def find_all_by_status(self, status: str):
        """Find all by status"""
        return self.collection.find({"status": status})

    def get_ready_to_send_for_campaign(
        self, campaign_id: int, limit: int = 100
    ):
        """Get ready to send emails for campaign"""
        return self.collection.find(
            {
                "status": MailingPoolStatus.READY_TO_SEND,
                "campaign_id": campaign_id,
            }
        ).limit(limit)

    def is_campaign_finished(self, campaign_id: int) -> bool:
        """Check if campaign is finished

        Campaign is considered `finished` if there are no emails of
        `init-like` status left: BEING_PROCESSED, MX_VALID, READY_TO_SEND
        """
        documents_count = self.collection.count_documents(
            {
                "$or": [
                    {"status": MailingPoolStatus.BEING_PROCESSED},
                    {"status": MailingPoolStatus.MX_VALID},
                    {"status": MailingPoolStatus.READY_TO_SEND},
                ],
                "campaign_id": campaign_id,
            }
        )

        return documents_count == 0
