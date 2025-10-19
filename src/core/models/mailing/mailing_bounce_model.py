"""Mailing Bounces Model"""

from django.conf import settings
from django.utils.timezone import now

from core.libs.mongo.db import get_mongo_connection
from core.models.enums import MailingBounceStatus

# flake8: noqa=E501


class MailingBounceManager:
    """Mailing bounce manager"""

    def __init__(self) -> None:
        client, database = get_mongo_connection()
        self.client = client
        self.database = database

        if settings.APP_ENV == "production":
            self.collection = self.database.wykladowcav2_mailing_bounces
        elif settings.APP_ENV == "staging":
            self.collection = self.database.wykladowcav2_mailing_bounces_staging
        else:
            self.collection = self.database.wykladowcav2_mailing_bounces_dev

    def close(self):
        """Close connection"""
        self.client.close()

    def upsert_bounce(
        self, message_id: str, sender_email: str, bounce_email: str, bounce_type: str
    ):
        """Upsert bounce into collection"""
        bounce_dict = {
            "sender_email": sender_email,
            "bounce_email": bounce_email,
            "bounce_type": bounce_type,
            "scanned_at": now(),
        }
        self.collection.update_one(
            {"_id": message_id},
            {"$set": {"_id": message_id, **bounce_dict}},
            upsert=True,
        )

    def is_email_bounced(self, email: str):
        """Check if email was bounced (any bounce type, any sender)"""
        return self.collection.find_one({"bounce_email": email})

    def is_email_bounced_permanent(self, email: str):
        """Check if email was bounced permanent (for any sender)"""
        return self.collection.find_one(
            {"bounce_email": email, "bounce_type": MailingBounceStatus.PERMANENT}
        )

    def is_email_bounced_temporary(self, email: str):
        """Check if email was bounced temporary (for any sender)"""
        return self.collection.find_one(
            {"bounce_email": email, "bounce_type": MailingBounceStatus.TEMPORARY}
        )

    def is_email_bounced_for_sender(self, sender_email: str, email: str):
        """Check if email was bounced for given sender (any bounce type)"""
        return self.collection.find_one(
            {"sender_email": sender_email, "bounce_email": email}
        )

    def is_email_bounced_permanent_for_sender(self, sender_email: str, email: str):
        """Check if email was bounced permanent for given sender"""
        return self.collection.find_one(
            {
                "sender_email": sender_email,
                "bounce_email": email,
                "bounce_type": MailingBounceStatus.PERMANENT,
            }
        )

    def is_email_bounced_temporary_for_sender(self, sender_email: str, email: str):
        """Check if email was bounced temporary for given sender"""
        return self.collection.find_one(
            {
                "sender_email": sender_email,
                "bounce_email": email,
                "bounce_type": MailingBounceStatus.TEMPORARY,
            }
        )
