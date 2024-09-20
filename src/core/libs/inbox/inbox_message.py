"""
Inbox message
"""

# flake8: noqa=E501
# pylint: disable=broad-exception-caught

import hashlib
import re
from email import message_from_bytes
from email.message import Message
from typing import Optional

from flufl.bounce import all_failures

from core.consts.aggressor_phrases import AGGRESSOR_PHRASES_ICONTAINS
from core.libs.normalizers import normalize_polish

from .decode_header import decode_header

EMAIL_REGEXP = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"


class InboxMessage:
    """Represents email mailbox message"""

    def __init__(self, message_bytes: bytes) -> None:
        self.message = message_from_bytes(message_bytes)

    def get_header(self, header_name: str, default_value: str = ""):
        """Get header"""
        return decode_header(self.message.get(header_name, default_value))

    @property
    def unique_hash(self) -> str:
        """Returns SHA256 hash of email string representation or Message-Id"""
        try:
            # Try to make sha256 hash of email content
            return hashlib.sha256(self.message.as_string().encode()).hexdigest()
        except UnicodeEncodeError:
            # If encoding error occurs fallbac to `Message-Id`
            return self.message_id_header

    @property
    def subject_header(self) -> str:
        """Returns email message `Subject` header"""
        return self.get_header("Subject")

    @property
    def date_header(self) -> str:
        """Returns email `Date` header"""
        return self.get_header("Date")

    @property
    def message_id_header(self) -> str:
        """Returns email `Message-Id` header"""
        return self.get_header("Message-Id")

    @property
    def from_header(self) -> str:
        """Returns email `From` header"""
        return self.get_header("From")

    @property
    def from_email(self) -> str:
        """Returns only email address from `From` header"""
        _from_header = self.from_header
        match = re.search(r"<([\w\W]+)>", _from_header)
        return (match.group(1) if match else _from_header).lower()

    def get_emails_permanent_failure(self):
        """Get permanent failures (emails) from message"""
        _, permanent = all_failures(self.message)
        return [str(_, "utf8").lower() for _ in permanent]

    def get_emails_temporary_failure(self):
        """Get temporary failures (emails) from message"""
        temporary, _ = all_failures(self.message)
        return [str(_, "utf8").lower() for _ in temporary]

    def is_vacation(self) -> bool:
        """Detect if email is a vaction message"""

        # Check if subject contains words indicating vacation
        phrases = [
            "nieobecn",
            "urlop",
            "urlopie",
            "abwesenheit",
            "przebywam na urlopie",
            "nieczynne biuro",
        ]
        for phrase in phrases:
            if phrase.lower() in self.subject_header.lower():
                return True
        return False

    def is_aggressor(self) -> bool:
        """Detect if email is aggressor"""

        # Check if subject contains words indicating vacation
        for phrase in AGGRESSOR_PHRASES_ICONTAINS:
            if any(
                [
                    phrase.lower() in self.subject_header.lower(),
                    phrase.lower() in self.get_content().lower(),
                ]
            ):
                return True
        return False

    def which_aggressor_phrases(self) -> list[str]:
        """Which aggressor phrases are contained in message"""
        ret: set[str] = set()
        for phrase in AGGRESSOR_PHRASES_ICONTAINS:
            if phrase.lower() in self.subject_header.lower():
                ret.add(f"subject: {phrase.lower()}")
            if phrase.lower() in self.get_content().lower():
                ret.add(f"content:{phrase.lower()}")
        return list(ret)

    def is_new_email(self) -> bool:
        """Detect if email is a info about new email"""

        # Check if subject contains words indicating vacation
        phrases = [
            "zmiana konta pocztowego",
            "nowy mail",
            "nowy email",
            "nowy e-mail",
            "nowe adres",
            "nowy adres",
        ]
        for phrase in phrases:
            if any(
                [
                    phrase.lower() in self.subject_header.lower(),
                    phrase.lower() in self.get_content().lower(),
                ]
            ):
                return True
        return False

    def is_reply(self) -> bool:
        """Detect if email message is a reply"""

        return "re:" in self.subject_header.lower()

    def is_bounce_by_subject(self) -> bool:
        """Check if email message's subject indicate bounce"""

        phrases = [
            "failure notice",
            "undeliverable",
            "undelivered",
            "delivery failed",
            "returned mail",
        ]
        for phrase in phrases:
            if phrase.lower() in self.subject_header.lower():
                return True
        return False

    def is_subject_resignation(self):
        """Does email message subject contains resignation"""
        subject = normalize_polish(self.subject_header)
        return any(
            [
                "rezygnacja" in subject,
                "wypis" in subject,
            ]
        )

    def get_subject_emails(self) -> list[str]:
        """Get emails from e-mail message subject"""
        subject = self.subject_header.lower()
        return list(set(re.findall(EMAIL_REGEXP, subject)))

    def get_content(self):
        """Get readable content of an email"""
        content_type_preferences = [  # order is important
            "text/html",
            "text/plain",
        ]

        parts_preferences: list[tuple[str, Message, Optional[str]]] = []

        # Get e-mail content parts
        # If email is multipart get all parts
        if self.message.is_multipart():
            for part in self.message.walk():
                content_type = part.get_content_type()
                content_charset = part.get_content_charset()
                parts_preferences.append((content_type, part, content_charset))
        # If email is not multipart just get only existing part
        else:
            content_type = self.message.get_content_type()
            content_charset = self.message.get_content_charset()
            parts_preferences.append((content_type, self.message, content_charset))

        fallback_content = "NO_CONTENT"

        # Try to return content only for preffered part types
        for content_type, part, content_charset in parts_preferences:
            for content_type_preference in content_type_preferences:
                # If part is of preffered type try to return decoded content
                if content_type_preference in content_type.lower():
                    decoded = part.get_payload(decode=True)

                    # If content charset is set then try to decode it with it
                    if content_charset:
                        try:
                            return decoded.decode(content_charset)  # type: ignore
                        except UnicodeDecodeError:
                            pass

                    # If given content charset is not correct fallback to utf8
                    try:
                        decoded = decoded.decode("utf8")  # type: ignore
                    except UnicodeDecodeError as exception:
                        fallback_content = f"Exception: {str(exception)}"
                    else:
                        return decoded

        return fallback_content
