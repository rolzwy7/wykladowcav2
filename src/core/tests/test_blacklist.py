# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=invalid-name

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

    def test_WhenEmailBlacklisted_ThenTrue(self):
        assert BlacklistService.is_email_blacklisted(BLACKLISTED_EMAIL) is True

    def test_WhenEmailNotBlacklisted_ThenFalse(self):
        assert BlacklistService.is_email_blacklisted(EMAIL) is False

    def test_WhenDomainBlacklisted_ThenTrue(self):
        assert (
            BlacklistService.is_domain_blacklisted(BLACKLISTED_DOMAIN) is True
        )

    def test_WhenDomainNotBlacklisted_ThenFalse(self):
        assert BlacklistService.is_domain_blacklisted(DOMAIN) is False

    def test_WhenPrefixBlacklisted_ThenTrue(self):
        assert (
            BlacklistService.is_prefix_blacklisted(BLACKLISTED_PREFIX) is True
        )

    def test_WhenPrefixNotBlacklisted_ThenFalse(self):
        assert BlacklistService.is_prefix_blacklisted(PREFIX) is False

    # def test_WhenPhraseBlacklisted_ThenTrue(self):
    #     phrases = [obj.phrase for obj in BlacklistedPhrase.objects.all()]
    #     test_data = [
    #         ("uodo@domain.pl", None),
    #         ("prefix@spam.com.pl", None),
    #         ("blacklisted.prefix@domain.pl", None),
    #         ("uodo@domain.pl", phrases),
    #         ("prefix@spam.com.pl", phrases),
    #         ("blacklisted.prefix@domain.pl", phrases),
    #     ]

    #     for td in test_data:
    #         email, phrases = td
    #         assert (
    #             BlacklistService.is_email_phrase_blacklisted(
    #                 email, phrases=phrases
    #             )
    #             is True
    #         )

    def test_WhenPhraseNotBlacklisted_ThenFalse(self):
        assert (
            BlacklistService.is_email_phrase_blacklisted(f"test@{PHRASE}.pl")
            is False
        )

    def test_WhenEmailDangerous_ThenTrue(self):
        assert (
            BlacklistService.is_email_dangerous_to_send("spam@domain.com")
            is True
        )
        assert (
            BlacklistService.is_email_dangerous_to_send("rodo@domain.com")
            is True
        )
        assert (
            BlacklistService.is_email_dangerous_to_send("uodo@domain.com")
            is True
        )

    def test_WhenEmailNotDangerous_ThenFalse(self):
        assert (
            BlacklistService.is_email_dangerous_to_send("biuro@domain.com")
            is False
        )
        assert (
            BlacklistService.is_email_dangerous_to_send("info@domain.com")
            is False
        )
        assert (
            BlacklistService.is_email_dangerous_to_send("kadry@domain.com")
            is False
        )
