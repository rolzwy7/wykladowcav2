"""
Mailing pool manager
"""

# flake8: noqa=E501

from datetime import datetime

from django.conf import settings
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from pymongo import DESCENDING, InsertOne, UpdateOne, errors

from core.libs.mongo.db import get_mongo_connection
from core.models.enums import MailingPoolStatus


class MailingPool(BaseModel):
    """Represents email bounce"""

    campaign_id: int
    email: str
    status: str
    priority: int
    bucket_id: int


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

    def create_insert_object(self, pool_object: MailingPool) -> InsertOne:
        """Insert pool object into collection"""
        new_id = f"{pool_object.campaign_id}:{pool_object.email}"
        return InsertOne({"_id": new_id, **pool_object.dict()})

    def bulk_write_ignore_errors(self, batch):
        """Bulk write ignoring errors"""
        try:
            self.collection.bulk_write(batch, ordered=False)
        except errors.BulkWriteError as e:
            pass

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
        self.collection.update_one({"_id": document_id}, {"$set": {"status": status}})

    def find_all_by_status(self, status: str):
        """Find all by status"""
        return self.collection.find({"status": status})

    def count_all_by_status(self, status: str):
        """Count all by status"""
        return self.collection.count_documents({"status": status})

    def find_all_by_status_and_campaign_ids(self, status: str, campaign_ids: list[int]):
        """Find all by status"""
        return self.collection.find(
            {"status": status, "campaign_id": {"$in": campaign_ids}}
        ).sort("priority", DESCENDING)

    def count_all_by_status_and_campaign_ids(
        self, status: str, campaign_ids: list[int]
    ):
        """count_all_by_status_and_campaign_ids"""
        return self.collection.count_documents(
            {"status": status, "campaign_id": {"$in": campaign_ids}}
        )

    def inc_todays_sent_counter_for_sender(self, sender: str):
        """inc_todays_sent_counter_for_sender"""

        collection = self.database[
            f"wykladowcav2_mailing_daily_counter_{settings.APP_ENV}"
        ]
        current_date = datetime.now().strftime("%Y-%m-%d")

        collection.update_one(
            {"_id": f"{current_date}:{sender}"},
            {
                "$inc": {"counter": 1},
                "$set": {
                    "current_date": current_date,
                    "sender": sender,
                },
            },
            upsert=True,
        )

    def inc_hourly_sent_counter_for_sender(self, sender: str):
        """inc_hourly_sent_counter_for_sender"""

        collection = self.database[
            f"wykladowcav2_mailing_hourly_counter_{settings.APP_ENV}"
        ]

        now_time = datetime.now()
        current_datehour = now_time.strftime("%Y-%m-%d %H")

        collection.update_one(
            {"_id": f"{current_datehour}:{sender}"},
            {
                "$inc": {"counter": 1},
                "$set": {
                    "datetime": now_time,
                    "sender": sender,
                },
            },
            upsert=True,
        )

    def inc_hourly_sent_counter_for_campaign(self, campaign_id: int):
        """inc_hourly_sent_counter_for_campaign"""

        collection = self.database[
            f"wykladowcav2_mailing_hourly_counter_{settings.APP_ENV}"
        ]
        now_time = datetime.now()
        current_datehour = now_time.strftime("%Y-%m-%d %H")

        collection.update_one(
            {"_id": f"{current_datehour}:campaign-id-{campaign_id}"},
            {
                "$inc": {"counter": 1},
                "$set": {
                    "datetime": now_time,
                    "campaign_id": campaign_id,
                },
            },
            upsert=True,
        )

    def get_todays_sent_counter_for_sender(self, sender: str, date_str=None):
        """get_todays_sent_counter_for_sender"""
        collection = self.database[
            f"wykladowcav2_mailing_daily_counter_{settings.APP_ENV}"
        ]
        if not date_str:
            current_date = datetime.now().strftime("%Y-%m-%d")
        else:
            current_date = date_str
        return collection.find_one({"_id": f"{current_date}:{sender}"})

    def inc_todays_sent_counter_for_campaign(self, campaign_id: int):
        """inc_todays_sent_counter_for_campaign"""

        collection = self.database[
            f"wykladowcav2_mailing_daily_counter_{settings.APP_ENV}"
        ]
        current_date = datetime.now().strftime("%Y-%m-%d")

        collection.update_one(
            {"_id": f"{current_date}:campaign-id-{campaign_id}"},
            {
                "$inc": {"counter": 1},
                "$set": {
                    "current_date": current_date,
                    "campaign_id": campaign_id,
                },
            },
            upsert=True,
        )

    def get_sent_counter_for_campaign(self, campaign_id: int, date_str=None):
        """get_todays_sent_counter_for_campaign"""
        collection = self.database[
            f"wykladowcav2_mailing_daily_counter_{settings.APP_ENV}"
        ]
        if not date_str:
            current_date = datetime.now().strftime("%Y-%m-%d")
        else:
            current_date = date_str
        return collection.find_one({"_id": f"{current_date}:campaign-id-{campaign_id}"})

    def get_ready_to_send_for_campaign(
        self, campaign_id: int, bucket_id: int, limit: int = 100
    ):
        """Get ready to send emails for campaign"""
        return (
            self.collection.find(
                {
                    "status": MailingPoolStatus.READY_TO_SEND,
                    "campaign_id": campaign_id,
                    "bucket_id": bucket_id,
                }
            )
            .sort("priority", DESCENDING)
            .limit(limit)
        )

    def is_campaign_finished(self, campaign_id: int) -> bool:
        """Check if campaign is finished

        Campaign is considered `finished` if there are no emails of
        `init-like` status left: BEING_PROCESSED, MX_VALID, READY_TO_SEND
        """
        document = self.collection.find_one(
            {
                "$or": [
                    {"status": MailingPoolStatus.BEING_PROCESSED},
                    {"status": MailingPoolStatus.MX_VALID},
                    {"status": MailingPoolStatus.READY_TO_SEND},
                ],
                "campaign_id": campaign_id,
            }
        )

        return bool(document)

    def randomize_buckets_ids(self, /, statuses: list[str], *, buckets_num: int = 4):
        """
        Randomize `bucket_id` field for pool items with given statuses

        Args:
            statuses (list[str]): list of statuses to affect
            buckets_num (int, optional): Number of buckets. Defaults to 4.
        """
        self.collection.update_many(
            {"status": {"$in": statuses}},
            [
                {
                    "$set": {
                        "bucket_id": {
                            "$floor": {"$multiply": [{"$rand": {}}, buckets_num + 1]}
                        }
                    }
                }
            ],
        )

    def delete_not_with_statuses(self, statuses: list[str]) -> int:
        """
        Delete pool items NOT with given statuses

        Args:
            statuses (list[str]): List of statuses to keep

        Returns:
            int: Number of deleted documents
        """
        return self.collection.delete_many(
            {"status": {"$not": {"$in": statuses}}}
        ).deleted_count
