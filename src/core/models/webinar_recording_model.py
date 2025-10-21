"""Webinar Recording Model"""

# flake8: noqa

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
    QuerySet,
    TextField,
    URLField,
    UUIDField,
)

from .enums import WebinarRecordingStatus


class WebinarRecordingManager(Manager):
    """WebinarRecordingManager query Manager"""

    ...


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
    recording_duration_seconds = PositiveIntegerField("Czas trwania nagrania (sekundy)")
    recorder_started = DateTimeField("Kiedy rozpoczęto nagrywanie")
    recording_file_size = CharField("Rozmiar nagrania", max_length=64)
    recording_name = CharField("Nazwa nagrania", max_length=500)

    class Meta:
        verbose_name = "Nagranie"
        verbose_name_plural = "Nagrania"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.recording_id}"


class WebinarRecordingTokenManager(Manager):
    """WebinarRecordingManager query Manager"""

    def get_tokens_by_participant_email(
        self, email: str
    ) -> QuerySet["WebinarRecordingToken"]:
        """Gets tokens by participant e-mail"""
        return self.get_queryset().filter(participant__email=email)

    def get_tokens_for_unique_recordings(self) -> list["WebinarRecordingToken"]:
        """Gets tokens for unique recordings"""

        all_tokens = self.get_queryset().all()
        ids = {}
        unique_tokens: list[WebinarRecordingToken] = []
        for rec_token in all_tokens:
            recording_id = rec_token.recording.recording_id
            if recording_id not in ids:
                unique_tokens.append(rec_token)
            ids[recording_id] = True

        return unique_tokens


class WebinarRecordingToken(Model):
    """Represents webinar's recording access token"""

    manager = WebinarRecordingTokenManager()

    created_at = DateTimeField(auto_now_add=True)

    token = UUIDField("Token nagrania", default=uuid.uuid4, unique=True)

    deny_access = BooleanField(
        "Odmówiono dostępu",
        default=False,
        help_text="Zaznacz aby odmówić dostępu do nagrania przez ten token",
    )

    starts_at = DateTimeField(
        "Ważny od",
        null=True,
        blank=True,
        help_text="Puste pole oznacza, że token jest ważny od momentu stworzenia",
    )

    expires_at = DateTimeField(
        "Ważny do",
        null=True,
        blank=True,
        help_text="Puste pole oznacza, że token nie wygasa nigdy",
    )

    recording = ForeignKey(
        "WebinarRecording", verbose_name="Nagranie", on_delete=CASCADE
    )

    free_access = BooleanField(
        "Otwarty dostęp",
        default=False,
        help_text="To nagranie jest dostępne dla każdego kto ma link",
    )

    password = CharField(
        "Hasło",
        max_length=64,
        blank=True,
        help_text="To nagranie jest zabezpieczone hasłem",
    )

    participant = ForeignKey(
        "WebinarParticipant",
        verbose_name="Uczestnik",
        on_delete=CASCADE,
        null=True,
        blank=True,
    )

    participant_extra_info = TextField("Dodatkowe informacje o uczestniku", blank=True)

    sale_recording_application = ForeignKey(
        "SaleRecordingApplication",
        verbose_name="Zgłoszenie - nagranie na sprzedaż",
        on_delete=CASCADE,
        null=True,
        blank=True,
    )

    sale_recording_participant = ForeignKey(
        "SaleRecordingParticipant",
        verbose_name="Uczestnik - nagranie na sprzedaż",
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
