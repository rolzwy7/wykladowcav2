import uuid

from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    PositiveIntegerField,
    URLField,
    UUIDField,
)

from .enums import WebinarRecordingStatus


class WebinarRecording(Model):
    """Represents webinar's recording"""

    created_at = DateTimeField(auto_now_add=True)

    is_visible = BooleanField(
        "Widoczne na stronie",
        default=True,
        help_text="Pokaż nagranie na stronie",
    )

    STATUS = [
        (WebinarRecordingStatus.DOWNLOADING, "W trakcie pobierania nagrania"),
        (WebinarRecordingStatus.DOWNLOADED, "Pobrano nagranie"),
        (
            WebinarRecordingStatus.FAILED,
            "Wystąpił błąd podczas pobierania",
        ),
    ]

    status = CharField(
        "Status",
        max_length=32,
        choices=STATUS,
        default=WebinarRecordingStatus.DOWNLOADING,
    )

    webinar = ForeignKey("Webinar", verbose_name="Webinar", on_delete=CASCADE)

    recording_id = CharField("ID nagrania", max_length=64, primary_key=True)
    recording_url = URLField("URL do pobrania nagrania")
    recording_duration_seconds = PositiveIntegerField(
        "Czas trwania nagrania (sekundy)"
    )
    recorder_started = DateTimeField("Kiedy rozpoczęto nagrywanie")
    recording_file_size = CharField("Rozmiar nagrania", max_length=64)
    recording_name = CharField("Nazwa nagrania", max_length=500)

    class Meta:
        verbose_name = "Nagranie"
        verbose_name_plural = "Nagrania"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.recording_id}"


class WebinarRecordingToken(Model):
    """Represents webinar's recording access token"""

    created_at = DateTimeField(auto_now_add=True)

    token = UUIDField("Token nagrania", default=uuid.uuid4, unique=True)

    deny_access = BooleanField(
        "Odmówiono dostępu",
        default=True,
        help_text="Zaznacz aby odmówić dostępu do nagrania przez ten token",
    )

    expires_at = DateTimeField(
        "Token wygasa",
        null=True,
        blank=True,
        help_text="Puste pole oznacza, że token nie wygasa nigdy",
    )

    recording = ForeignKey(
        "WebinarRecording", verbose_name="Nagranie", on_delete=CASCADE
    )

    participant = ForeignKey(
        "WebinarParticipant",
        verbose_name="Uczestnik",
        on_delete=CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Nagranie (token)"
        verbose_name_plural = "Nagrania (tokeny)"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.token}"
