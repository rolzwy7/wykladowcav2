from django.test import TestCase


class NormalizersTestCase(TestCase):
    def test_WhenAggressiveEmailSubject_ThenDetectCorrectly(self):
        ...  # TODO: test_WhenAggressiveEmailSubject_ThenDetectCorrectly

    def test_WhenAggressiveEmailContent_ThenDetectCorrectly(self):
        ...  # TODO: test_WhenAggressiveEmailContent_ThenDetectCorrectly

    def test_WhenVacationEmailSubject_ThenDetect(self):
        ...  # TODO: test_WhenVacationEmailSubject_ThenDetect

    def test_WhenNoVacationEmailSubject_ThenDontDetect(self):
        ...  # TODO: test_WhenNoVacationEmailSubject_ThenDontDetect
