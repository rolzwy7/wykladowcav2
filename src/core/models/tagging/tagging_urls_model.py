from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.mongo.db import get_mongo_connection


class TaggedUrl(BaseModel):
    """Represents tagged url"""

    url: str
    tags: list[str]
    content: str
    created_at: int
    built_at: int  # last built with browser


class TaggedUrlManager:
    """Tagged url manager"""

    def __init__(self) -> None:
        client, database = get_mongo_connection()
        self.client = client
        self.database = database
        self.collection = self.database.wykladowcav2_tagging_url

    def close(self):
        """Close connection"""
        self.client.close()

    # TODO

    # def get_or_create_tagged_email(self, email: str):
    #     """Create new tagged e-mail

    #     Args:
    #         email (str): email address

    #     Returns:
    #         bool: True if new document created, False otherwise
    #     """

    #     document = self.collection.find_one({"_id": email})
    #     if not document:
    #         document = self.collection.insert_one({"_id": email, "tags": []})
    #     return document

    # def add_tags_to_email(self, email: str, tags: list[str]):
    #     """Add given tags to e-mail"""
    #     self.collection.update_one(
    #         {"_id": email}, {"$addToSet": {"tags": {"$each": tags}}}
    #     )

    # def delete_tags_from_email(self, email: str, tags: list[str]):
    #     """Delete given tags from e-mail"""
    #     self.collection.update_one(
    #         {"_id": email}, {"$pull": {"tags": {"$in": tags}}}
    #     )

    # def get_untagged_emails(self):
    #     """Get e-mails with no tags"""
    #     return self.collection.find({"tags": []})

    # def find_emails_by_tags(self, tags: list[str]):
    #     """Find emails by tags"""
    #     return self.collection.find({"tags": {"$in": tags}})
