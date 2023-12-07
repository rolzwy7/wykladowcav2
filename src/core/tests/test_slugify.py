# pylint: disable=invalid-name
from django.test import TestCase

from core.utils.text import slugify


class SlugifyTestCase(TestCase):
    """Slugify test case"""

    def test_When_CalledCorrectly_Then_SlugifyCorrectly(self):
        """Assert that custom slugify works"""
        assert slugify("a---a") == "a-a"
        assert slugify("a  -a") == "a-a"
        assert slugify(" __a __ a__ ") == "a-__-a"
        assert slugify("ABC") == "abc"
        assert slugify("ĄĆĘŁŃÓŚŻŹ") == "acelnoszz"
        assert slugify("ąćęłńóśżź") == "acelnoszz"
        assert slugify("Przemysław Pogłódek") == "przemyslaw-poglodek"
