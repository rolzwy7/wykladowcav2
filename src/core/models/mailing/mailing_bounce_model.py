from django.conf import settings
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from pymongo import UpdateOne

from core.libs.mongo.db import get_mongo_connection


class MailingBounce(BaseModel):
    """Represents email bounce"""

    id: str
    email: str
    bounce_type: str
    content: str


class MailingBounceManager:
    """Mailing bounce manager"""

    def __init__(self) -> None:
        client, database = get_mongo_connection()
        self.client = client
        self.database = database
        if settings.APP_ENV == "production":
            self.collection = self.database.wykladowcav2_mailing_bounces
        else:
            self.collection = self.database.wykladowcav2_mailing_bounces_dev

    def close(self):
        """Close connection"""
        self.client.close()

    def create_upsert_object(self, bounce: MailingBounce):
        """Upsert bounce into collection"""
        new_id = bounce.id
        bounce_dict = bounce.dict()
        del bounce_dict["id"]
        return UpdateOne(
            {"_id": new_id},
            {"$set": {"_id": new_id, **bounce_dict}},
            upsert=True,
        )

    def upsert_documents(self, bounces: list[MailingBounce]) -> None:
        """Upsert document into bounces collection"""
        if bounces:
            self.collection.bulk_write(
                [self.create_upsert_object(bounce) for bounce in bounces]
            )

    def is_email_bounced(self, email: str):
        """Check if email was bounced"""
        return self.collection.find_one({"email": email})
