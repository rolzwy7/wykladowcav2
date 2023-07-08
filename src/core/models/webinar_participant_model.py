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

from .enums import ApplicationStatus, WebinarParticipantIsMxValidType
from .webinar_model import Webinar


class WebinarParticipantManager(Manager):
    """WebinarParticipant query Manager"""

    def get_participants_from_sent_applications(
        self, webinar: Webinar
    ) -> QuerySet["WebinarParticipant"]:
        """Get participants from applications marked as `sent`"""
        return self.get_queryset().filter(
            # Only participants from applications that have been sent
            Q(application__webinar=webinar)
            & Q(application__status=ApplicationStatus.SENT)
        )


class WebinarParticipant(Model):
    """Represents webinar participant"""

    manager = WebinarParticipantManager()

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

    IS_MX_VALID = [
        (WebinarParticipantIsMxValidType.NOT_CHECKED, "Nie sprawdzono"),
        (WebinarParticipantIsMxValidType.INVALID, "MX ustawiony"),
        (WebinarParticipantIsMxValidType.VALID, "brak MX"),
    ]

    is_mx_valid = CharField(
        max_length=32,
        choices=IS_MX_VALID,
        default=WebinarParticipantIsMxValidType.NOT_CHECKED,
    )

    def __str__(self) -> str:
        return f"Metadata for webinar participant {self.id}"  # type: ignore
