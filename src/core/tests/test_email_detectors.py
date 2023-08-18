from core_app.libs.email.detectors import detect_vacation_from_subject
from django.test import TestCase


class NormalizersTestCase(TestCase):
    def test_WhenAggressiveEmailSubject_ThenDetectCorrectly(self):
        ...

    def test_WhenAggressiveEmailContent_ThenDetectCorrectly(self):
        ...

    def test_WhenVacationEmailSubject_ThenDetect(self):
        assert (
            detect_vacation_from_subject("Nieobecność: Harmonogram webinarów")
            is True
        )
        assert (
            detect_vacation_from_subject("Nieobecności w pracy : Harmonogram")
            is True
        )
        assert detect_vacation_from_subject("informacja o nieobecności") is True
        assert detect_vacation_from_subject("urlop") is True
        assert detect_vacation_from_subject("informacja o urlopie") is True
        assert (
            detect_vacation_from_subject(
                "Automatyczna odpowiedź - nieobecnosc w pracy"
            )
            is True
        )

    def test_WhenNoVacationEmailSubject_ThenDontDetect(self):
        assert detect_vacation_from_subject("some neutral subject") is False
