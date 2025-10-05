"""
Mailing pool manager
"""

# flake8: noqa=E501

from django.conf import settings
from django.utils.timezone import now

from core.libs.mongo.db import get_mongo_connection


class MailingDuplicateSendsManager:
    """MailingDuplicateSendsManager"""

    def __init__(self) -> None:
        client, database = get_mongo_connection()
        self.client = client
        self.database = database

        if settings.APP_ENV == "production":
            self.collection = self.database.wykladowcav2_mailing_duplicates
        elif settings.APP_ENV == "staging":
            self.collection = self.database.wykladowcav2_mailing_duplicates_staging
        else:
            self.collection = self.database.wykladowcav2_mailing_duplicates_dev

    def close(self):
        """Close connection"""
        self.client.close()

    def is_email_already_sent_today(self, email: str) -> bool:
        """is_email_already_sent_today"""
        yyyy_mm_dd = now().strftime("%Y-%m-%d")
        return bool(self.collection.find_one({"_id": f"{yyyy_mm_dd}-{email}"}))

    def mark_email_sent_today(self, email: str):
        """Mark email as sent today in the collection"""
        yyyy_mm_dd = now().strftime("%Y-%m-%d")
        self.collection.update_one(
            {"_id": f"{yyyy_mm_dd}-{email}"},
            {"$set": {"_id": f"{yyyy_mm_dd}-{email}"}},
            upsert=True,
        )
