"""
Test domain blacklist detection
"""

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=invalid-name
# flake8: noqa=E501
# pylint: disable=line-too-long

from django.test import TestCase

from core.models import BlacklistedDomain
from core.services import BlacklistService

NOT_BLACKLISTED_DOMAIN = "somedomain.com"
BLACKLISTED_DOMAIN = "blacklisted.com"


class DetectBlacklistedDomainTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        BlacklistedDomain(domain=BLACKLISTED_DOMAIN).save()

    def test_When_DomainBlacklisted_Then_Detect(self):
        assert BlacklistService.is_domain_blacklisted(BLACKLISTED_DOMAIN) is True

    def test_When_DomainNotBlacklisted_Then_DontDetect(self):
        assert BlacklistService.is_domain_blacklisted(NOT_BLACKLISTED_DOMAIN) is False
