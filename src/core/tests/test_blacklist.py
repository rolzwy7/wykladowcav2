# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=invalid-name
# flake8: noqa=E501
# pylint: disable=line-too-long

from django.test import TestCase

from core.models import (
    BlacklistedDomain,
    BlacklistedEmail,
    BlacklistedPhrase,
    BlacklistedPrefix,
)
from core.services import BlacklistService

EMAIL = "notblacklisted@test.com"
BLACKLISTED_EMAIL = "blacklisted@test.com"

DOMAIN = "somedomain.com"
BLACKLISTED_DOMAIN = "blacklisted.com"

PREFIX = "someprefix"
BLACKLISTED_PREFIX = "rodo"

PHRASE = "notblacklistedphrase"
BLACKLISTED_PHRASES = [
    "uodo@",
    "@spam.",
    "blacklisted.",
]


class BlacklistUnitTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        BlacklistedEmail(email=BLACKLISTED_EMAIL).save()
        BlacklistedDomain(domain=BLACKLISTED_DOMAIN).save()
        BlacklistedPrefix(prefix=BLACKLISTED_PREFIX).save()
        for blacklisted_phrase in BLACKLISTED_PHRASES:
            BlacklistedPhrase(phrase=blacklisted_phrase).save()

    def test_When_EmailBlacklisted_Then_Detect(self):
        assert BlacklistService.is_email_blacklisted(BLACKLISTED_EMAIL) is True

    def test_When_EmailNotBlacklisted_Then_DontDetect(self):
        assert BlacklistService.is_email_blacklisted(EMAIL) is False

    def test_When_DomainBlacklisted_Then_Detect(self):
        assert BlacklistService.is_domain_blacklisted(BLACKLISTED_DOMAIN) is True

    def test_When_DomainNotBlacklisted_Then_DontDetect(self):
        assert BlacklistService.is_domain_blacklisted(DOMAIN) is False

    def test_When_PhraseBlacklisted_Then_Detect(self):
        assert (
            BlacklistService.is_email_phrase_blacklisted(BLACKLISTED_PHRASES[0]) is True
        )

    def test_When_PhraseNotBlacklisted_Then_DontDetect(self):
        assert (
            BlacklistService.is_email_phrase_blacklisted(f"test@{PHRASE}.pl") is False
        )

    def test_WhenEmail_Dangerous_Then_Detect(self):
        assert BlacklistService.is_email_dangerous_to_send("spam@domain.com") is True
        assert BlacklistService.is_email_dangerous_to_send("rodo@domain.com") is True
        assert BlacklistService.is_email_dangerous_to_send("uodo@domain.com") is True

    def test_When_EmailNotDangerous_Then_DontDetect(self):
        assert BlacklistService.is_email_dangerous_to_send("biuro@domain.com") is False
        assert BlacklistService.is_email_dangerous_to_send("info@domain.com") is False
        assert BlacklistService.is_email_dangerous_to_send("kadry@domain.com") is False
