"""Mailing resignations manager"""

# flake8: noqa=E501

from random import choice, shuffle
from string import ascii_letters, digits
from typing import Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.mongo.db import get_mongo_connection


class MailingTracking(BaseModel):
    """Represents mailing tracking"""

    email: str


class MailingTrackingManager:
    """Mailing tracking manager"""

    def __init__(self) -> None:
        client, database = get_mongo_connection()
        self.client = client
        self.database = database
        self.collection = self.database.wykladowcav2_mailing_tracking

    def close(self):
        """Close connection"""
        self.client.close()

    def generate_unused_tracking_code(self, length: int = 10) -> str:
        """Generate unused tracking code without saving it"""
        random_base = list(f"{ascii_letters}{digits}")
        shuffle(random_base)

        for _ in range(1_000):
            code_candid = "".join([choice(random_base) for _ in range(length)])
            document = self.collection.find_one({"_id": code_candid})
            if document is None:
                return code_candid

        return ""

    def get_or_create_tracking(self, email: str):
        """Get or create tracking for given email"""
        document = self.collection.find_one({"email": email})

        # If exists, return
        if document:
            return document

        # If doesn't exist, create and return
        tracking_code = self.generate_unused_tracking_code()
        document = MailingTracking(email=email).dict()
        self.collection.insert_one({"_id": tracking_code, **document})
        return {"_id": tracking_code, **document}

    def get_tracking_by_code(self, code: str):
        """Get tracking by code"""
        return self.collection.find_one({"_id": code})

    def get_tracking_by_email(self, code: str):
        """Get tracking by email"""
        return self.collection.find_one({"email": code})
