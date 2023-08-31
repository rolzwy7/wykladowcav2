from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    ForeignKey,
    Manager,
    Model,
    OneToOneField,
    Q,
    QuerySet,
)

from .enums import (
    ApplicationStatus,
    WebinarParticipantIsMxValidType,
    WebinarParticipantStatus,
)
from .webinar_model import Webinar


class WebinarParticipantManager(Manager):
    """WebinarParticipant query Manager"""

    def get_valid_participants_for_webinar(
        self, webinar: Webinar
    ) -> QuerySet["WebinarParticipant"]:
        """Get valid participants for given webinar"""
        return self.get_queryset().filter(
            # For given webinar
            Q(application__webinar=webinar)
            # Only from sent applications
            & Q(application__status=ApplicationStatus.SENT)
            # Only participating
            & Q(status=WebinarParticipantStatus.PARTICIPATING)
        )

    # TODO: kinda cringe
    def get_valid_participants_for_application(
        self, application  # don't use typing, circular import
    ) -> QuerySet["WebinarParticipant"]:
        """Get valid participants for given application"""
        return self.get_queryset().filter(
            # For given application
            Q(application=application)
            # Only from sent applications
            & Q(application__status=ApplicationStatus.SENT)
            # Only participating
            & Q(status=WebinarParticipantStatus.PARTICIPATING)
        )


class WebinarParticipant(Model):
    """Represents webinar participant"""

    manager = WebinarParticipantManager()

    STATUS = [
        (WebinarParticipantStatus.PARTICIPATING, "Uczestniczy w szkoleniu"),
        (WebinarParticipantStatus.RESIGNATION, "Rezygnacja ze szkolenia"),
    ]

    status = CharField(
        max_length=32,
        default=WebinarParticipantStatus.PARTICIPATING,
        choices=STATUS,
    )

    application = ForeignKey(
        "WebinarApplication", on_delete=CASCADE, verbose_name="Zgłoszenie"
    )
    first_name = CharField("Imię", max_length=100)
    last_name = CharField("Nazwisko", max_length=100)
    email = CharField("E-mail", max_length=100)
    phone = CharField("Numer telefonu", max_length=100, blank=True)

    class Meta:
        verbose_name = "Uczestnik"
        verbose_name_plural = "Uczestnicy"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def fullname(self):
        """Get participant fullname"""
        return f"{self.first_name} {self.last_name}"


class WebinarParticipantMetadata(Model):
    """Represents webinar participant's metadata"""

    participant = OneToOneField(
        "WebinarParticipant", on_delete=CASCADE, verbose_name="Uczestnik"
    )

    phoned = BooleanField("Czy zadzwoniono przed szkoleniem?", default=False)
    clickmeeting_invitation_send = BooleanField(
        "Czy wysłano zaproszenie do clickmeeting?", default=False
    )

    IS_MX_VALID = [
        (WebinarParticipantIsMxValidType.NOT_CHECKED, "Nie sprawdzono"),
        (WebinarParticipantIsMxValidType.INVALID, "MX nie istnieje"),
        (WebinarParticipantIsMxValidType.VALID, "MX poprawny"),
    ]

    is_mx_valid = CharField(
        max_length=32,
        choices=IS_MX_VALID,
        default=WebinarParticipantIsMxValidType.NOT_CHECKED,
    )

    def __str__(self) -> str:
        return f"Metadata for webinar participant {self.id}"  # type: ignore
