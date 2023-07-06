from django.test import TestCase


class WebinarTestCase(TestCase):
    def test_WhenWebinarBeforeDate_ThenPresentInHomepage(self):
        """
        If `now` is before `webinar.date`, webinar must be
        present in homepage queryset and not present in
        archive queryset
        """
        ...  # TODO: Test

    def test_WhenWebinarDateWithinDelay_ThenPresentInHomepage(self):
        """
        If `now` is after `webinar.date`, but before
        `webinar.date` + WEBINAR_ARCHIVE_DELAY_MINUTES
        then it should be present in homepage queryset
        and not present in archive queryset
        """
        ...  # TODO: Test

    def test_WhenWebinarArchived_ThenPresentInArchive(self):
        """
        If `now` is after `webinar.date` + WEBINAR_ARCHIVE_DELAY_MINUTES
        then it should be present in archive queryset and not present
        in homepage queryset
        """
        ...  # TODO: Test
