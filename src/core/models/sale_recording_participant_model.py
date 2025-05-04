"""Webinar Participant Model Admin"""

# flake8: noqa=E501

from django.db.models import (
    CASCADE,
    CharField,
    DateField,
    ForeignKey,
    Manager,
    Model,
    Q,
    QuerySet,
)

from core.models import SaleRecordingApplication


class SaleRecordingParticipantManager(Manager):
    """WebinarParticipant query Manager"""

    def get_all_participants_for_application(
        self,
        application: SaleRecordingApplication,
    ) -> QuerySet["SaleRecordingApplication"]:
        """Get all participants for given application (even not valid)"""
        return self.get_queryset().filter(
            # For given application
            Q(application=application)
        )


class SaleRecordingParticipant(Model):
    """Represents sale recording participant"""

    manager = SaleRecordingParticipantManager()

    STATUS = [
        ("INIT", "Init"),
        ("ACCESS_SENT", "Wysłano dostęp do nagrania"),
    ]

    status = CharField(
        max_length=32,
        default="",
        choices=STATUS,
    )

    application = ForeignKey(
        "SaleRecordingApplication", on_delete=CASCADE, verbose_name="Zamówienie"
    )
    first_name = CharField("Imię", max_length=100)
    last_name = CharField("Nazwisko", max_length=100)
    email = CharField("E-mail", max_length=100)
    access_from = DateField("Dostęp od dnia", null=True, blank=True)

    class Meta:
        """Meta"""

        verbose_name = "Uczestnik (nagranie na sprzedaż)"
        verbose_name_plural = "Uczestnicy (nagranie na sprzedaż)"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.email})"

    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)

    @property
    def fullname(self):
        """Get participant fullname"""
        return f"{self.first_name} {self.last_name}"
