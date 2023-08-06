from pydantic import BaseModel  # pylint: disable=no-name-in-module
from pymongo import UpdateOne

from core.libs.mongo.db import get_mongo_connection


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
        return self.database.wykladowcav2_mailing_pool.count_documents(
            {"campaign_id": campaign_id}
        )

    def group_by_count_statuses(self, campaign_id: int):
        """Perform group-by-count operation on statuses"""
        return self.database.wykladowcav2_mailing_pool.aggregate(
            [
                {"$match": {"campaign_id": campaign_id}},
                {"$group": {"_id": "$status", "count": {"$sum": 1}}},
            ]
        )

    def change_status(self, document_id: str, status: str) -> None:
        """Change status of pool object"""
        self.database.wykladowcav2_mailing_pool.update_one(
            {"_id": document_id}, {"$set": {"status": status}}
        )

    def find_all_by_status(self, status: str):
        """Find all by status"""
        return self.database.wykladowcav2_mailing_pool.find({"status": status})
