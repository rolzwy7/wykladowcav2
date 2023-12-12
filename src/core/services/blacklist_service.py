"""
Blacklist service
"""

# flake8: noqa=E501

import re

from django.db.models import Q
from django.utils.timezone import now, timedelta

from core.consts import DANGEROUSE_PHRASES
from core.models.blacklist import (
    BlacklistAggressor,
    BlacklistedDomain,
    BlacklistedEmail,
    BlacklistedEmailTemporary,
    BlacklistedPhrase,
    BlacklistedPrefix,
)

EMAIL_REGEXP = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"


class BlacklistService:
    """Blacklist service"""

    def __init__(self) -> None:
        pass

    @staticmethod
    def is_email_dangerous_to_send(email: str):
        """Check if email is dangerous to send by checking phrases"""
        for dangerouse_phrase in DANGEROUSE_PHRASES:
            if dangerouse_phrase.lower() in email.lower():
                return True
        return False

    @staticmethod
    def is_domain_blacklisted(domain: str) -> bool:
        """Check if domain is blacklisted"""
        return BlacklistedDomain.manager.filter(domain=domain.lower()).exists()

    @staticmethod
    def blacklist_domain(domain: str) -> None:
        """Blacklist domain"""
        BlacklistedDomain.manager.get_or_create(domain=domain.lower())

    @staticmethod
    def is_email_blacklisted(email: str) -> bool:
        """Check if email is blacklisted"""
        return BlacklistedEmail.manager.filter(email=email.lower()).exists()

    @staticmethod
    def blacklist_email(email: str) -> None:
        """Blacklist email"""
        BlacklistedEmail.manager.get_or_create(email=email.lower())

    @staticmethod
    def is_email_temporarily_blacklisted(email: str) -> bool:
        """Check if email is temporarily blacklisted"""
        return BlacklistedEmailTemporary.manager.filter(
            Q(email=email.lower()) & Q(expires_at__gt=now())
        ).exists()

    @staticmethod
    def blacklist_email_temporarily(email: str) -> None:
        """Blacklist email temporarily"""
        obj, _ = BlacklistedEmailTemporary.manager.get_or_create(email=email.lower())
        obj.expires_at = now() + timedelta(days=10)
        obj.save()

    @staticmethod
    def is_email_phrase_blacklisted(email: str):
        """Check if there is blacklisted phrase in email"""
        phrases = [_.phrase for _ in BlacklistedPhrase.manager.all()]
        for phrase in phrases:
            if phrase.lower() in email.lower():
                return True
        return False

    @staticmethod
    def blacklist_phrase(phrase: str) -> None:
        """Blacklist phrase"""
        BlacklistedPhrase.manager.get_or_create(phrase=phrase.lower())

    @staticmethod
    def is_prefix_blacklisted(prefix: str):
        """Check if email prefix is blacklisted"""
        return BlacklistedPrefix.manager.filter(prefix=prefix.lower()).exists()

    @staticmethod
    def blacklist_prefix(prefix: str) -> None:
        """Blacklist prefix"""
        BlacklistedPrefix.manager.get_or_create(prefix=prefix.lower())

    @staticmethod
    def is_email_aggressor(email: str):
        """Check if email is an aggressor"""
        return BlacklistAggressor.manager.filter(email=email.lower()).exists()

    @staticmethod
    def blacklist_aggressor(email: str):
        """Blacklist aggressor"""
        return BlacklistAggressor.manager.get_or_create(email=email.lower())

    @staticmethod
    def try_to_blacklist_line(line: str) -> tuple[bool, str]:
        """Detect what kind of blacklist the `line` is then blacklist

        Args:
            line (str): line to be blacklisted

        Returns:
            bool: True when blacklisted, False if skipped
        """

        if len(line) <= 5:
            return False, line

        if re.match(EMAIL_REGEXP, line):  # email
            email = line
            BlacklistService.blacklist_email(email)
            blacklist_type = "EMAIL:"
        elif line.startswith("@"):  # domain
            domain = line.strip("@")
            BlacklistService.blacklist_domain(domain)
            blacklist_type = "DOMENA:"
        elif line.endswith("@"):  # prefix
            prefix = line.strip("@")
            BlacklistService.blacklist_prefix(prefix)
            blacklist_type = "PREFIKS:"
        else:  # phrase
            phrase = line
            BlacklistService.blacklist_phrase(phrase)
            blacklist_type = "FRAZA:"

        return True, f"{blacklist_type} `{line}`"
