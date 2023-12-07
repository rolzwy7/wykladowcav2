"""
Test prefix blacklist detection
"""

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=invalid-name
# flake8: noqa=E501
# pylint: disable=line-too-long

from django.test import TestCase

from core.models import BlacklistedPrefix
from core.services import BlacklistService

NOT_BLACKLISTED_PREFIX = "not_blacklisted_prefix"
BLACKLISTED_PREFIX = "blacklisted_prefix"


class DetectBlacklistedPrefixTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        BlacklistedPrefix(prefix=BLACKLISTED_PREFIX).save()

    def test_When_PrefixBlacklisted_Then_Detect(self):
        assert BlacklistService.is_prefix_blacklisted(BLACKLISTED_PREFIX) is True

    def test_When_PrefixNotBlacklisted_Then_DontDetect(self):
        assert BlacklistService.is_prefix_blacklisted(NOT_BLACKLISTED_PREFIX) is False
