"""
Test email blacklist detection
"""

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=invalid-name
# flake8: noqa=E501
# pylint: disable=line-too-long

from django.test import TestCase

from core.models import BlacklistedEmail
from core.services import BlacklistService

NOT_BLACKLISTED_EMAIL = "notblacklisted@test.com"
BLACKLISTED_EMAIL = "blacklisted@test.com"


class DetectBlacklistedEmailTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        BlacklistedEmail(email=BLACKLISTED_EMAIL).save()

    def test_When_EmailBlacklisted_Then_Detect(self):
        assert BlacklistService.is_email_blacklisted(BLACKLISTED_EMAIL) is True

    def test_When_EmailNotBlacklisted_Then_DontDetect(self):
        assert BlacklistService.is_email_blacklisted(NOT_BLACKLISTED_EMAIL) is False
