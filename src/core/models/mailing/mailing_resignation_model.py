"""Mailing resignations manager"""

# flake8: noqa=E501

from random import choice, shuffle
from string import ascii_letters, digits
from typing import Optional

from django.utils.timezone import now
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.mongo.db import get_mongo_connection


class MailingResignation(BaseModel):
    """Represents mailing resignation"""

    email: str
    confirmed: bool
    resignation_list: Optional[str]


class MailingResignationManager:
    """Mailing resignation manager"""

    def __init__(self) -> None:
        client, database = get_mongo_connection()
        self.client = client
        self.database = database
        self.collection = self.database.wykladowcav2_mailing_resignations

    def close(self):
        """Close connection"""
        self.client.close()

    def generate_unused_resignation_code(self, length: int = 10) -> str:
        """Generate unused discount code without saving it"""
        random_base = list(f"{ascii_letters}{digits}")
        shuffle(random_base)

        for _ in range(1_000):
            code_candid = "".join([choice(random_base) for _ in range(length)])
            document = self.collection.find_one({"_id": code_candid})
            if document is None:
                return code_candid

        return ""

    def get_or_create_resignation(
        self, email: str, resignation_list: Optional[str] = None
    ):
        """Get or create unconfirmed resignation for given email"""
        document = self.collection.find_one(
            {"email": email, "resignation_list": resignation_list}
        )

        # If exists, return
        if document:
            return document

        # If doesn't exist, create and return
        resignation_code = self.generate_unused_resignation_code()
        document = MailingResignation(
            email=email, confirmed=False, resignation_list=resignation_list
        ).dict()
        self.collection.insert_one({"_id": resignation_code, **document})
        return {"_id": resignation_code, **document}

    def get_by_resignation_code(self, code: str):
        """Get resignation by resignation code"""
        return self.collection.find_one({"_id": code})

    def get_by_resignation_code_and_list(self, code: str, resignation_list: str):
        """Get resignation by resignation code"""
        return self.collection.find_one(
            {"_id": code, "resignation_list": resignation_list}
        )

    def is_resignation(self, email: str, resignation_list: str) -> bool:
        """Is email in confirmed resignations"""
        document = self.collection.find_one(
            {"email": email, "resignation_list": resignation_list, "confirmed": True}
        )
        return document is not None

    def mark_confirmed_by_email(self, email: str) -> None:
        """Mark resignation as cofirmed by email"""
        self.collection.update_one({"email": email}, {"$set": {"confirmed": True}})

    def mark_resignation_as_manual(self, email: str) -> None:
        """Mark resignation as manual (by form)"""
        self.collection.update_one({"email": email}, {"$set": {"manual": True}})

    def mark_confirmed_by_code(self, code: str) -> None:
        """Mark resignation as cofirmed by code"""
        self.collection.update_one({"_id": code}, {"$set": {"confirmed": True}})

    def mark_confirmed_by_code_and_list(self, code: str, resignation_list: str) -> None:
        """Mark resignation as cofirmed by code and list"""
        self.collection.update_one(
            {"_id": code, "resignation_list": resignation_list},
            {"$set": {"confirmed": True, "resignation_at": now()}},
        )
