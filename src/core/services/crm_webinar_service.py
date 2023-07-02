from core.models import Webinar, WebinarApplication, WebinarParticipant


class CrmWebinarService:
    """Service for CRM webinar"""

    def __init__(self, webinar: Webinar) -> None:
        self.webinar = webinar

    def sent_applications(self):
        """Returns all `sent` applications for this webinar"""
        return WebinarApplication.manager.sent_applications(self.webinar)

    def gathered_participants(self):
        """Participants from `sent` applications"""
        return (
            WebinarParticipant.manager.get_participants_from_sent_applications(
                self.webinar
            )
        )

    def total_netto_value_of_webinar(self):
        """Return total NETTO value of this webinar"""
        sent_applications = self.sent_applications()
        return sum(
            [
                application.participants.count() * application.price_netto
                for application in sent_applications
            ]
        )

    def get_context(self):
        """Number of gathered participants"""
        gathered_participants = self.gathered_participants()
        return {
            "webinar": self.webinar,
            "sent_applications": self.sent_applications(),
            "gathered_participants": gathered_participants,
            "gathered_participants_count": gathered_participants.count(),
            "total_netto_value_of_webinar": self.total_netto_value_of_webinar(),
        }
