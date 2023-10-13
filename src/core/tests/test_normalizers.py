from django.test import TestCase

from core.libs.normalizers import normalize_polish


class NormalizersTestCase(TestCase):
    def test_WhenTextProvided_ThenNormalizerWorksCorrectly(self):
        assert normalize_polish("Kość") == "kosc"
        assert normalize_polish("WąS") == "was"
        assert normalize_polish("ąćęłńśóżź") == "acelnsozz"
        assert normalize_polish("ą1ć2ę3ł4ń5ś6ó7ż8ź") == "a1c2e3l4n5s6o7z8z"
        assert normalize_polish("Kość!!@@") == "kosc!!@@"
        assert normalize_polish("## Ko ść!!@@") == "## ko sc!!@@"
