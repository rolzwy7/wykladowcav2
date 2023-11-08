# flake8: noqa:E501
# pylint: disable=line-too-long
# pylint: disable=import-outside-toplevel

from core.models import User, Webinar, WebinarApplication, WebinarApplicationSubmitter
from core.models.enums import ApplicationStatus


class ApplicationSummaryService:
    """Service for application summary"""

    def __init__(
        self, application: WebinarApplication, user: User, webinar: Webinar
    ) -> None:
        self.application = application
        self.user = user
        self.webinar = webinar

    def send_application(self, dispatch: bool = True) -> None:
        """Send application for webinar"""

        # Set application status as sent
        self.application.status = ApplicationStatus.SENT

        # Get submitter
        submitter: WebinarApplicationSubmitter = self.application.submitter  # type: ignore

        # If user authenticated then connect
        if self.user.is_authenticated:
            self.application.user = self.user

        # Decrement webinar's remaining places
        self.webinar.remaining_places = max(0, self.webinar.remaining_places - 1)

        # Save changes
        self.application.save()
        self.webinar.save()

        # Dispatch tasks after application send
        if dispatch:
            from core.tasks_dispatch import after_application_sent_dispatch

            after_application_sent_dispatch(self.application, submitter)
