"""
Test phrase blacklist detection
"""

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=invalid-name
# flake8: noqa=E501
# pylint: disable=line-too-long

from django.test import TestCase

from core.models import BlacklistedPhrase
from core.services import BlacklistService

NOT_BLACKLISTED_PHRASE = "notblacklisted"
BLACKLISTED_PHRASE = "uodo@"


class BlacklistUnitTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        BlacklistedPhrase(phrase=BLACKLISTED_PHRASE).save()

    def test_When_PhraseBlacklisted_Then_Detect(self):
        assert BlacklistService.is_email_phrase_blacklisted(BLACKLISTED_PHRASE) is True

    def test_When_PhraseNotBlacklisted_Then_DontDetect(self):
        assert (
            BlacklistService.is_email_phrase_blacklisted(
                f"test@{NOT_BLACKLISTED_PHRASE}.pl"
            )
            is False
        )
