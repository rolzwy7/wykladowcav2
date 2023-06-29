from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    ForeignKey,
    Model,
    OneToOneField,
)

from .enums import WebinarParticipantIsMxValidType


class WebinarParticipant(Model):
    """Represents webinar participant"""

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


class WebinarParticipantMetadata(Model):
    """Represents webinar participant's metadata"""

    participant = OneToOneField(
        "WebinarParticipant", on_delete=CASCADE, verbose_name="Uczestnik"
    )
    phoned = BooleanField(default=False)

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

    confirmation_email_opened = BooleanField(default=False)
