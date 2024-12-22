"""CRM webinar service"""

# flake8: noqa:E501
# pylint: disable=line-too-long

from django.db.models import Count, Q, QuerySet

from core.models import (
    ConferenceEdition,
    ConferenceFreeParticipant,
    MailingCampaign,
    Webinar,
    WebinarApplication,
    WebinarApplicationCancellation,
    WebinarApplicationMetadata,
    WebinarApplicationTracking,
    WebinarAsset,
    WebinarCertificate,
    WebinarMetadata,
    WebinarMoveRegister,
    WebinarParticipant,
    WebinarParticipantMetadata,
    WebinarRecording,
    WebinarRecordingToken,
)


class CrmWebinarService:
    """Service for CRM webinar"""

    def __init__(self, webinar: Webinar) -> None:
        self.webinar = webinar

    def get_move_registers(self):
        """Get move registers for this webinar"""
        return WebinarMoveRegister.manager.filter(webinar=self.webinar).order_by(
            "-created_at"
        )

    def get_applications_cancellations(self):
        """Get cancellations for applications of this webinar"""
        return (
            WebinarApplicationCancellation.objects.filter(  # pylint: disable=no-member
                application__webinar=self.webinar
            )
        )

    def get_sent_applications(self):
        """Returns all sent applications for this webinar"""
        return WebinarApplication.manager.sent_applications_for_webinar(self.webinar)

    def get_applications_with_additional_infos(
        self, applications: QuerySet[WebinarApplication]
    ):
        """Returns applications that have additional infos set"""
        return [
            application
            for application in applications
            if application.additional_information
        ]

    def get_sent_applications_metadata(self):
        """Returns metadatas from sent applications metadata"""
        application_ids = [_.id for _ in self.get_sent_applications()]  # type: ignore
        return WebinarApplicationMetadata.objects.filter(  # pylint: disable=no-member
            application__in=application_ids
        )

    def get_unfinished_applications(self):
        """Returns all unfinished applications for this webinar"""
        return WebinarApplication.manager.unfinished_applications_for_webinar(
            self.webinar
        )

    def get_got_to_summary_applications(self):
        """Returns all unfinished applications that got to summary"""
        return WebinarApplication.manager.unfinished_applications_for_webinar(
            self.webinar
        ).filter(got_to_summary=True)

    def get_resigned_applications(self):
        """Returns all resigned applications for this webinar"""
        return WebinarApplication.manager.resigned_applications_for_webinar(
            self.webinar
        )

    def get_gathered_participants(self):
        """Participants that are `valid` for this webinar"""
        return WebinarParticipant.manager.get_valid_participants_for_webinar(
            self.webinar
        )

    def get_uncertain_participants_count(self):
        """Get uncertain participant count"""
        return WebinarParticipantMetadata.objects.filter(
            Q(participant__application__webinar=self.webinar) & Q(uncertain=True)
        ).count()

    def get_certificates(self):
        """Get certificates for gathered participants"""
        return WebinarCertificate.objects.filter(  # pylint: disable=no-member
            participant__in=self.get_gathered_participants()
        )

    def get_recordings(self):
        """Get all recordings for this webinar"""
        return WebinarRecording.manager.filter(webinar=self.webinar)

    def get_all_recording_tokens(self):
        """Get all tokens for all recordings for this webinar"""
        return WebinarRecordingToken.manager.filter(recording__webinar=self.webinar)

    def lecturer_price_netto(self) -> int:
        """Get lecturer's NETTO price for this webinar"""
        metatada, _ = (
            WebinarMetadata.objects.get_or_create(  # pylint: disable=no-member
                webinar=self.webinar
            )
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
        sent_applications = self.get_sent_applications()

        return sum(
            [
                WebinarParticipant.manager.get_valid_participants_for_application(
                    application=application
                ).count()
                * application.price_netto
                for application in sent_applications
            ]
        )

    def get_expected_income(self) -> int:
        """Get expected income which is `total_netto` - `lecturer_netto`"""
        total_netto = self.total_netto_value_of_webinar()
        lecturer_netto = self.lecturer_price_netto()
        return total_netto - lecturer_netto

    def get_participant_duplicates(
        self, participants: QuerySet[WebinarParticipant]
    ) -> list[str]:
        """Check if there are participants duplicates"""
        emails, emails_dups = [], []
        for participant in participants:
            if participant.email in emails:
                emails_dups.append(participant.email)
            else:
                emails.append(participant.email)

        return emails_dups

    def get_application_duplicates(
        self, applications: QuerySet[WebinarApplication]
    ) -> tuple[list[str], list[str]]:
        """Get duplicates of buyer's and recipient's NIPs"""
        buyer_nips, buyer_nips_dups = [], []
        recipient_nips, recipient_nips_dups = [], []
        for application in applications:
            # Buyer
            if application.buyer:
                nip = application.buyer.nip
                if nip in buyer_nips:
                    buyer_nips_dups.append(nip)
                else:
                    buyer_nips.append(nip)
            # Recipient
            if application.recipient:
                nip = application.recipient.nip
                if nip in recipient_nips:
                    recipient_nips_dups.append(nip)
                else:
                    recipient_nips.append(nip)

        return buyer_nips_dups, recipient_nips_dups

    def get_groupby_application_type_count(self):
        """Get count for each application type"""
        queryset = (
            self.get_sent_applications()
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
            for _ in queryset
        ]

    def get_webinar_assets(self):
        """Get webinar's assets"""
        return WebinarAsset.manager.get_for_webinar(webinar=self.webinar)

    def get_webinar_rating(
        self,
        gathered_participants_count: int,
        click_count_mailing: int,
        click_count_facebook: int,
        lecturer_price_netto: int,
        total_netto_value_of_webinar: int,
    ) -> float:
        """Get webinar rating"""
        # Facebook clicks
        fb_click_score = min(25, (click_count_facebook / 300) * 25)
        mailing_click_score = min(15, (click_count_mailing / 1_000) * 15)
        participants_score = min(35, (gathered_participants_count / 15) * 35)

        if lecturer_price_netto:
            netto_base = total_netto_value_of_webinar - lecturer_price_netto
        else:
            netto_base = max(0, total_netto_value_of_webinar - 2500)

        netto_score = min(25, (netto_base / 10_000) * 25)

        score_sum = sum(
            [
                fb_click_score,
                mailing_click_score,
                participants_score,
                netto_score,
            ]
        )

        return score_sum

    def get_free_participants(self) -> list[ConferenceFreeParticipant]:
        """_summary_"""

        ret: list[ConferenceFreeParticipant] = []

        try:
            edition: ConferenceEdition = ConferenceEdition.manager.get(
                webinar=self.webinar
            )
        except ConferenceEdition.DoesNotExist:  # pylint: disable=no-member
            return ret

        return list(ConferenceFreeParticipant.manager.filter(edition=edition))

    def get_application_tracking(self) -> QuerySet[WebinarApplicationTracking]:
        """_summary_"""

        return WebinarApplicationTracking.objects.filter(webinar=self.webinar)

    def get_context(self):
        """Number of gathered participants"""
        gathered_participants = self.get_gathered_participants().order_by("first_name")
        gathered_participants_count = gathered_participants.count()
        total_netto_value_of_webinar = self.total_netto_value_of_webinar()
        webinar_assets_count = self.get_webinar_assets().count()
        lecturer_price_netto = self.lecturer_price_netto()
        sent_applications = self.get_sent_applications().order_by("-created_at")
        unfinished_applications = self.get_unfinished_applications()
        got_to_summary_applications = self.get_got_to_summary_applications()
        resigned_applications = self.get_resigned_applications()
        recordings = self.get_recordings()
        certificates = self.get_certificates()
        webinar_metadata = WebinarMetadata.objects.get(  # pylint: disable=no-member
            webinar=self.webinar
        )
        additional_infos_applications = self.get_applications_with_additional_infos(
            sent_applications
        )
        additional_infos_applications_count = len(additional_infos_applications)
        buyer_nip_dups, recipient_nip_dups = self.get_application_duplicates(
            sent_applications
        )
        participant_email_dups = self.get_participant_duplicates(gathered_participants)
        free_participants = self.get_free_participants()

        try:
            conference_edition = ConferenceEdition.manager.get(webinar=self.webinar)
        except ConferenceEdition.DoesNotExist:  # pylint: disable=no-member
            conference_edition = None

        return {
            "webinar": self.webinar,
            "is_fake": self.webinar.is_fake,
            "is_confirmed": self.webinar.is_confirmed,
            "is_hidden": self.webinar.is_hidden,
            "grouping_token": self.webinar.grouping_token,
            "free_participants": free_participants,
            "uncertain_participants_count": self.get_uncertain_participants_count(),
            "application_tracking_codes": self.get_application_tracking(),
            # Conference
            "conference_edition": conference_edition,
            # Sent applications
            "sent_applications": sent_applications,
            "sent_applications_count": sent_applications.count(),
            # Unfinished applications
            "unfinished_applications": unfinished_applications,
            "unfinished_applications_count": unfinished_applications.count(),
            # `got_to_summary` applications
            "got_to_summary_applications": got_to_summary_applications,
            "got_to_summary_applications_count": got_to_summary_applications.count(),
            # Resigned applications
            "resigned_applications": resigned_applications,
            "resigned_applications_count": resigned_applications.count(),
            # Gathered participants
            "gathered_participants": gathered_participants,
            "gathered_participants_count": gathered_participants_count,
            # Applications with additional infos
            "additional_infos_applications": additional_infos_applications,
            "additional_infos_applications_count": additional_infos_applications_count,
            # Recordings
            "recordings": recordings,
            "recordings_count": recordings.count(),
            # Recordings
            "certificates": certificates,
            "certificates_count": certificates.count(),
            # Clicks
            "click_count_mailing": webinar_metadata.click_count_mailing,
            "click_count_facebook": webinar_metadata.click_count_facebook,
            "click_count_onesignal": webinar_metadata.click_count_onesignal,
            # Webinar rating
            "webinar_rating": self.get_webinar_rating(
                gathered_participants_count,
                webinar_metadata.click_count_mailing,
                webinar_metadata.click_count_facebook,
                lecturer_price_netto,
                total_netto_value_of_webinar,
            ),
            # Other
            "lecturer_netto_price": lecturer_price_netto,
            "lecturer_netto_price_display": f"{lecturer_price_netto:,}",
            "total_netto_value_of_webinar": total_netto_value_of_webinar,
            "total_netto_value_of_webinar_display": f"{total_netto_value_of_webinar:,}",
            "get_groupby_application_type_count": self.get_groupby_application_type_count(),
            "webinar_assets_count": webinar_assets_count,
            "buyer_nip_duplicates": buyer_nip_dups,
            "recipient_nip_duplicates": recipient_nip_dups,
            "participant_email_duplicates": participant_email_dups,
            # Mailing campaign
            "mailing_campaigns": MailingCampaign.manager.filter(
                webinar=self.webinar
            ).order_by("created_at"),
        }

    def get_upcoming_webinar_row_context(self):
        """Number of gathered participants"""
        gathered_participants = self.get_gathered_participants().order_by("first_name")
        gathered_participants_count = gathered_participants.count()
        total_netto_value_of_webinar = self.total_netto_value_of_webinar()
        webinar_assets_count = self.get_webinar_assets().count()
        lecturer_price_netto = self.lecturer_price_netto()
        sent_applications = self.get_sent_applications().order_by("-created_at")
        unfinished_applications = self.get_unfinished_applications()
        webinar_metadata = WebinarMetadata.objects.get(  # pylint: disable=no-member
            webinar=self.webinar
        )
        free_participants = self.get_free_participants()
        is_default_program = "[Program Szkolenia]" in self.webinar.program

        try:
            conference_edition = ConferenceEdition.manager.get(webinar=self.webinar)
        except ConferenceEdition.DoesNotExist:  # pylint: disable=no-member
            conference_edition = None

        return {
            "webinar": self.webinar,
            "is_fake": self.webinar.is_fake,
            "is_confirmed": self.webinar.is_confirmed,
            "is_hidden": self.webinar.is_hidden,
            "conference_edition": conference_edition,
            "free_participants": free_participants,
            "sent_applications_count": sent_applications.count(),
            "gathered_participants_count": gathered_participants_count,
            "uncertain_participants_count": self.get_uncertain_participants_count(),
            "total_netto_value_of_webinar": total_netto_value_of_webinar,
            "total_netto_value_of_webinar_display": f"{total_netto_value_of_webinar:,}",
            "lecturer_netto_price": lecturer_price_netto,
            "lecturer_netto_price_display": f"{lecturer_price_netto:,}",
            "webinar_rating": self.get_webinar_rating(
                gathered_participants_count,
                webinar_metadata.click_count_mailing,
                webinar_metadata.click_count_facebook,
                lecturer_price_netto,
                total_netto_value_of_webinar,
            ),
            "unfinished_applications_count": unfinished_applications.count(),
            # Clicks
            "click_count_mailing": webinar_metadata.click_count_mailing,
            "click_count_facebook": webinar_metadata.click_count_facebook,
            "click_count_onesignal": webinar_metadata.click_count_onesignal,
            # Mailing campaign
            "mailing_campaigns": MailingCampaign.manager.filter(
                webinar=self.webinar
            ).order_by("created_at"),
            "webinar_assets_count": webinar_assets_count,
            "is_default_program": is_default_program,
        }
