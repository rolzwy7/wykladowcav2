# pylint: disable=broad-exception-caught

import hashlib
import re
from email import message_from_bytes
from email.message import Message
from typing import Optional

from flufl.bounce import all_failures

from core.libs.normalizers import normalize_polish

from .decode_header import decode_header


class InboxMessage:
    """Represents email mailbox message"""

    def __init__(self, message_bytes: bytes) -> None:
        self.message = message_from_bytes(message_bytes)

    def get_header(self, header_name: str, default_value: str = ""):
        """Get header"""
        return decode_header(self.message.get(header_name, default_value))

    @property
    def unique_hash(self):
        """Returns SHA256 hash of email string representation"""
        return hashlib.sha256(self.message.as_string().encode()).hexdigest()

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
            "Nieobecność",
            "Nieobecności",
            "urlop",
            "urlopie",
            "Abwesenheit",
        ]
        for phrase in phrases:
            is_match = normalize_polish(phrase) in normalize_polish(
                self.subject_header
            )

            if is_match:
                return True

        return False

    def is_resignation(self):
        """Is email message a resignation"""
        subject = normalize_polish(self.subject_header)
        return any(
            [
                "rezygnacja" in subject,
                "wypis" in subject,
            ]
        )

    def get_content(self):
        """Get readable content of an email"""
        content_type_preferences = [
            "text/html",
            "text/plain",
        ]

        parts_preferences: list[tuple[str, Message, Optional[str]]] = []

        # Get parts
        if self.message.is_multipart():
            for part in self.message.walk():
                content_type = part.get_content_type()
                content_charset = part.get_content_charset()
                parts_preferences.append((content_type, part, content_charset))
        else:
            content_type = self.message.get_content_type()
            content_charset = self.message.get_content_charset()
            parts_preferences.append(
                (content_type, self.message, content_charset)
            )

        fallback_content = ""

        # Try to return content
        for content_type, part, content_charset in parts_preferences:
            for content_type_preference in content_type_preferences:
                if content_type_preference in content_type.lower():
                    if content_charset:
                        return part.get_payload(decode=True).decode(
                            content_charset
                        )
                    else:
                        decoded = part.get_payload(decode=True)
                        try:
                            decoded = decoded.decode("utf8")
                        except Exception as exception:
                            fallback_content = str(exception)
                        else:
                            return decoded

        return fallback_content
