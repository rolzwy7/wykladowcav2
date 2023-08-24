from django.conf import settings

from core.libs.mongo.db import get_mongo_connection


class MailingProcessingCacheManager:
    """MailingProcessingCache pool manager"""

    def __init__(self) -> None:
        client, database = get_mongo_connection()
        self.client = client
        self.database = database

        if settings.APP_ENV == "production":
            self.collection = self.database.wykladowcav2_mailing_cache
        elif settings.APP_ENV == "staging":
            self.collection = self.database.wykladowcav2_mailing_cache_staging
        else:
            self.collection = self.database.wykladowcav2_mailing_cache_dev

    def close(self):
        """Close connection"""
        self.client.close()

    def insert_message_id_into_cache(self, message_id: str) -> None:
        """Inserts message ID into mongo cache"""
        self.collection.update_one(
            {"_id": message_id}, {"$set": {"_id": message_id}}, upsert=True
        )

    def is_in_cache(self, message_id: str) -> bool:
        """Check if message ID is in cache"""
        return self.collection.find_one({"_id": message_id}) is not None

    def get_all_cached_message_ids(self) -> list[str]:
        """Returns all cached messages ids as a list"""
        return [document["_id"] for document in self.collection.find({})]
