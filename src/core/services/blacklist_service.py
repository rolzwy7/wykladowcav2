from django.db.models import Q
from django.utils.timezone import now, timedelta

from core.consts import DANGEROUSE_PHRASES
from core.models import (
    BlacklistedDomain,
    BlacklistedEmail,
    BlacklistedEmailTemporary,
    BlacklistedPhrase,
    BlacklistedPrefix,
)


class BlacklistService:
    """Blacklist service"""

    def __init__(self) -> None:
        pass

    @staticmethod
    def is_email_dangerous_to_send(email: str):
        """Check if email is dangerous to send by checking phrases"""
        for dangerouse_phrase in DANGEROUSE_PHRASES:
            if dangerouse_phrase in email.lower():
                return True
        return False

    @staticmethod
    def is_domain_blacklisted(domain: str) -> bool:
        """Check if domain is blacklisted"""
        return BlacklistedDomain.objects.filter(domain=domain.lower()).exists()

    @staticmethod
    def blacklist_domain(domain: str) -> None:
        """Blacklist domain"""
        BlacklistedDomain.objects.get_or_create(domain=domain)

    @staticmethod
    def is_email_blacklisted(email: str) -> bool:
        """Check if email is blacklisted"""
        return BlacklistedEmail.objects.filter(email=email.lower()).exists()

    @staticmethod
    def blacklist_email(email: str) -> None:
        """Blacklist email"""
        BlacklistedEmail.objects.get_or_create(email=email)

    @staticmethod
    def is_email_temporarily_blacklisted(email: str) -> bool:
        """Check if email is temporarily blacklisted"""
        return BlacklistedEmailTemporary.objects.filter(
            Q(email=email.lower()) & Q(expires_at__gt=now())
        ).exists()

    @staticmethod
    def blacklist_email_temporarily(email: str) -> None:
        """Blacklist email temporarily"""
        obj, created = BlacklistedEmailTemporary.objects.get_or_create(
            email=email
        )
        if not created:
            obj.expires_at = now() + timedelta(days=14)
            obj.save()

    @staticmethod
    def is_email_phrase_blacklisted(email: str):
        """Check if there is blacklisted phrase in email"""
        phrases = [_.phrase for _ in BlacklistedPhrase.objects.all()]
        for phrase in phrases:
            if phrase.lower() in email.lower():
                return True
        return False

    @staticmethod
    def is_prefix_blacklisted(prefix: str):
        """Check if email prefix is blacklisted"""
        return BlacklistedPrefix.objects.filter(prefix=prefix.lower()).exists()
