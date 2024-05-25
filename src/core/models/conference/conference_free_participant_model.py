# flake8: noqa

import uuid

from django.db.models import (
    RESTRICT,
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
    ForeignKey,
    Manager,
    Model,
    UUIDField,
)


class ConferenceFreeParticipantManager(Manager):
    """ConferenceFreeParticipantManager"""

    ...


class ConferenceFreeParticipant(Model):
    """Represents CRM Company"""

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    manager = ConferenceFreeParticipantManager()

    edition = ForeignKey("ConferenceEdition", on_delete=RESTRICT, verbose_name="Edycja")

    first_name = CharField("Imię", max_length=64)

    last_name = CharField("Nazwisko", max_length=64)

    watch_token = UUIDField("Token panelu oglądania", default=uuid.uuid4)

    VOIVODESHIPS = [
        ("DOLNOŚLĄSKIE", "Dolnośląskie"),
        ("KUJAWSKO-POMORSKIE", "Kujawsko-pomorskie"),
        ("LUBELSKIE", "Lubelskie"),
        ("LUBUSKIE", "Lubuskie"),
        ("ŁÓDZKIE", "Łódzkie"),
        ("MAŁOPOLSKIE", "Małopolskie"),
        ("MAZOWIECKIE", "Mazowieckie"),
        ("OPOLSKIE", "Opolskie"),
        ("PODKARPACKIE", "Podkarpackie"),
        ("PODLASKIE", "Podlaskie"),
        ("POMORSKIE", "Pomorskie"),
        ("ŚLĄSKIE", "Śląskie"),
        ("ŚWIĘTOKRZYSKIE", "Świętokrzyskie"),
        ("WARMIŃSKO-MAZURSKIE", "Warmińsko-mazurskie"),
        ("WIELKOPOLSKIE", "Wielkopolskie"),
        ("ZACHODNIOPOMORSKIE", "Zachodniopomorskie"),
    ]

    voivodeship = CharField("Województwo", max_length=32, choices=VOIVODESHIPS)

    phone = CharField("Telefon", max_length=32)

    email = EmailField("Adres e-mail", max_length=32)

    KNOW_FROM = [
        ("EMAIL", "Wiadomość e-mail"),
        ("FACEBOOK", "Facebook"),
        ("PHONE", "Telefonicznie"),
        ("INTERNET", "W internecie"),
        ("FRIEND", "Od znajomego"),
        ("COWORKER", "Od współpracownika"),
        ("PUSH", "Powiadomienie na komórce"),
    ]

    know_from = CharField(
        "Skąd dowiedziałeś się o szkoleniu?", max_length=32, choices=KNOW_FROM
    )

    USING_CLOSED_WEBINARS = [
        ("YES", "TAK"),
        ("NO", "NIE"),
    ]

    using_closed_webinars = CharField(
        "Czy korzystasz ze szkoleń zamkniętych w swojej firmie lub jednostce?",
        max_length=10,
        choices=USING_CLOSED_WEBINARS,
    )

    consent = BooleanField("Zgody marketingowe", default=False)

    class Meta:
        verbose_name = "Konferencja (darmowy uczestnik)"
        verbose_name_plural = "Konferencje (darmowy uczestnik)"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)
