import uuid

from django.conf import settings
from django.db.models import (
    CASCADE,
    CharField,
    DateField,
    DateTimeField,
    ForeignKey,
    Model,
    TextField,
    UUIDField,
)
from django.urls import reverse

BASE_URL = settings.BASE_URL


class WebinarCertificate(Model):
    """Represents webinar certificate"""

    created_at = DateTimeField(auto_now_add=True)

    uuid = UUIDField(
        "Identyfikator certyfikatu", default=uuid.uuid4, unique=True
    )

    first_name = CharField("Imię", max_length=100)
    last_name = CharField("Nazwisko", max_length=100)

    title = TextField("Tytuł szkolenia")

    issue_date = DateField("Data wystawienia")

    hours = CharField(
        "Czas trwania", max_length=20, help_text="Przykład: `4 godziny`"
    )

    participant = ForeignKey(
        "WebinarParticipant",
        verbose_name="Uczestnik",
        on_delete=CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Certyfikat"
        verbose_name_plural = "Certyfikaty"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def absolute_url(self) -> str:
        """Get absolute URL for this certificate

        Returns:
            str: absolute url to certificate
        """
        certificate_path = reverse(
            "core:certificate_pdf_page", kwargs={"uuid": self.uuid}
        )
        return f"{BASE_URL}{certificate_path}"
