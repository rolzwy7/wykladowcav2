from core.models import WebinarApplication, WebinarParticipant


class ApplicationService:
    """Application service"""

    def __init__(self, application: WebinarApplication) -> None:
        self.application = application

    def get_valid_participants(self):
        """Get valid participants for this application"""
        return (
            WebinarParticipant.manager.get_valid_participants_for_application(
                application=self.application
            )
        )

    def get_all_participants(self):
        """Get all participants for this application"""
        return WebinarParticipant.manager.get_all_participants_for_application(
            application=self.application
        )

    def get_total_price_netto(self):
        """Get total price NETTO for this application"""
        price_netto = self.application.price_netto
        return self.get_valid_participants().count() * price_netto

    def get_preview_total_price_netto(self):
        """Get preview of total price NETTO

        Used in application summary page
        """
        price_netto = self.application.price_netto
        return self.get_all_participants().count() * price_netto
