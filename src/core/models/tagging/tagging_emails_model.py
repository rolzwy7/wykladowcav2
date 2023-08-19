from time import time

from pydantic import BaseModel  # pylint: disable=no-name-in-module
from pymongo import UpdateOne

from core.libs.mongo.db import get_mongo_connection


class TaggedEmail(BaseModel):
    """Represents tagged email"""

    email: str
    tags: list[str]
    created_at: int


class TaggedEmailManager:
    """Tagged email manager"""

    def __init__(self) -> None:
        client, database = get_mongo_connection()
        self.client = client
        self.database = database
        self.collection = self.database.wykladowcav2_tagging_email

    def close(self):
        """Close connection"""
        self.client.close()

    def create_upsert_object(self, email: str, tags: list[str]) -> UpdateOne:
        """Create upsert object"""
        prefix, domain = email.split("@")
        return UpdateOne(
            {"_id": email},
            {
                "$set": {
                    "_id": email,
                    "tags": {"$addToSet": {"tags": {"$each": tags}}},
                    "created_at": int(time()),
                    "prefix": prefix,
                    "domain": domain,
                }
            },
            upsert=True,
        )

    def get_tagged_email(self, email: str):
        """Get tagged email"""
        return self.collection.find_one({"_id": email})

    def get_or_create_tagged_email(self, email: str):
        """Create new tagged e-mail

        Args:
            email (str): email address

        Returns:
            bool: True if new document created, False otherwise
        """

        document = self.get_tagged_email(email)

        if document is None:
            prefix, domain = email.split("@")
            self.collection.insert_one(
                {
                    "_id": email,
                    "tags": [],
                    "created_at": int(time()),
                    "prefix": prefix,
                    "domain": domain,
                }
            )
            document = self.get_tagged_email(email)

        return document

    def add_tags_to_email(self, email: str, tags: list[str]):
        """Add given tags to e-mail"""
        self.collection.update_one(
            {"_id": email}, {"$addToSet": {"tags": {"$each": tags}}}
        )

    def delete_tags_from_email(self, email: str, tags: list[str]):
        """Delete given tags from e-mail"""
        self.collection.update_one(
            {"_id": email}, {"$pull": {"tags": {"$in": tags}}}
        )

    def get_untagged_emails(self):
        """Get e-mails with no tags"""
        return self.collection.find({"tags": []})

    def get_all_emails_count(self):
        """Get all e-mails count"""
        return self.collection.count_documents({})

    def get_untagged_emails_count(self):
        """Get untagged e-mails count"""
        return self.collection.count_documents({"tags": []})

    def find_emails_by_tags(self, tags: list[str]):
        """Find emails by tags"""
        return self.collection.find({"tags": {"$in": tags}})

    # TODO: Add tags by regexp
    # TODO: Remove tags by regexp
