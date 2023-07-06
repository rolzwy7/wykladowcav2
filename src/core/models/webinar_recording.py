import uuid

from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Manager,
    Model,
    PositiveIntegerField,
    URLField,
    UUIDField,
)

from .enums import WebinarRecordingStatus


class WebinarRecordingManager(Manager):
    """Webinar recording query Manager"""

    ...  # TODO: WebinarRecordingManager


class WebinarRecording(Model):
    """Represents webinar's recording"""

    manager = WebinarRecordingManager()

    created_at = DateTimeField(auto_now_add=True)

    is_visible = BooleanField(
        "Widoczne na stronie",
        default=True,
        help_text="Pokaż nagranie na stronie",
    )

    STATUS = [
        (WebinarRecordingStatus.DOWNLOADING, "Pobieranie nagrania w trakcie"),
        (WebinarRecordingStatus.DOWNLOADED, "Pobrano nagranie"),
        (
            WebinarRecordingStatus.FAILED,
            "Wystąpił błąd podczas pobierania",
        ),
        (WebinarRecordingStatus.CONVERTED, "Przekonwertowany do MPEG-DASH"),
    ]

    status = CharField(
        "Status", choices=STATUS, default=WebinarRecordingStatus.DOWNLOADING
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


class WebinarRecordingToken(Model):
    """Represents webinar's recording access token"""

    created_at = DateTimeField(auto_now_add=True)

    # TODO: access counter ?

    token = UUIDField("Token nagrania", default=uuid.uuid4, unique=True)

    is_active = BooleanField(
        "Czy token jest aktywny",
        default=True,
        help_text="Odznacz, aby siłowo odmówić dostępu",
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
        verbose_name = "Token nagrania"
        verbose_name_plural = "Tokeny nagrań"
        ordering = ["-created_at"]
