# flake8: noqa:E501
from django.db.models import Count

from core.models import (
    Webinar,
    WebinarApplication,
    WebinarAsset,
    WebinarMetadata,
    WebinarParticipant,
)


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

    def lecturer_price_netto(self) -> int:
        """Get lecturer's NETTO price for this webinar"""
        metatada, _ = WebinarMetadata.objects.get_or_create(
            webinar=self.webinar
        )
        return metatada.lecturer_price_netto

    def get_percent_goal(self) -> int:
        """Get % of webinar netto value divided by lecturer netto price

        Example:
        - 0.50 would mean that so far 50% of value necessary to realize
        webinar have been gathered
        """
        total_netto = self.total_netto_value_of_webinar()
        lecturer_netto = self.lecturer_price_netto()
        if lecturer_netto == 0:
            return 0
        else:
            return int(100 * (total_netto / lecturer_netto))

    def total_netto_value_of_webinar(self):
        """Return total NETTO value of this webinar"""
        sent_applications = self.sent_applications()
        return sum(
            [
                application.participants.count() * application.price_netto
                for application in sent_applications
            ]
        )

    def get_expected_income(self) -> int:
        """Get expected income which is `total_netto` - `lecturer_netto`"""
        total_netto = self.total_netto_value_of_webinar()
        lecturer_netto = self.lecturer_price_netto()
        return total_netto - lecturer_netto

    def get_groupby_application_type_count(self):
        """Get count for each application type"""
        qs = (
            self.sent_applications()
            .values("application_type")
            .annotate(count=Count("application_type"))
        )

        _translate_map = {
            dbkey: name for (dbkey, name) in WebinarApplication.APPLICATION_TYPE
        }

        return [
            (
                _translate_map.get(_["application_type"], "?"),
                _["application_type"],
                _["count"],
            )
            for _ in qs
        ]

    def get_webinar_assets(self):
        """Get webinar's assets"""
        return WebinarAsset.manager.get_for_webinar(webinar=self.webinar)

    def get_context(self):
        """Number of gathered participants"""
        gathered_participants = self.gathered_participants()
        total_netto_value_of_webinar = self.total_netto_value_of_webinar()
        webinar_assets_count = self.get_webinar_assets().count()
        lecturer_price_netto = self.lecturer_price_netto()
        sent_applications = self.sent_applications()
        return {
            "webinar": self.webinar,
            "sent_applications": sent_applications,
            "sent_applications_count": sent_applications.count(),
            "gathered_participants": gathered_participants,
            "gathered_participants_count": gathered_participants.count(),
            "lecturer_netto_price": lecturer_price_netto,
            "lecturer_netto_price_display": f"{lecturer_price_netto:,}",
            "total_netto_value_of_webinar": total_netto_value_of_webinar,
            "total_netto_value_of_webinar_display": f"{total_netto_value_of_webinar:,}",
            "get_groupby_application_type_count": self.get_groupby_application_type_count(),
            "webinar_assets_count": webinar_assets_count,
        }
