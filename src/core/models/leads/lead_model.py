"""
Lead model
"""
# flake8: noqa:E501
# pylint: disable=line-too-long
import uuid

from django.db.models import (
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
    Manager,
    ManyToManyField,
    Model,
    UUIDField,
)

from core.models.enums import LeadSource


class LeadManager(Manager):
    """Lead query Manager"""

    ...


class LeadModel(Model):
    """This model represents Lecturer"""

    manager = LeadManager()

    # Creation & Update dates
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    # Basic data
    email = EmailField("Adres E-mail", primary_key=True)
    first_name = CharField("Imię", max_length=100, blank=True)
    last_name = CharField("Nazwisko", max_length=100, blank=True)
    phone = CharField("Telefon", max_length=32, blank=True)

    # Flags
    is_subscribed = BooleanField("Czy subskrybuje?", default=False)
    was_activated = BooleanField("Czy aktywował przez e-mail?", default=False)
    was_customer = BooleanField("Czy był klientem?", default=False)
    detected_bot_click = BooleanField("Wykryto kliknięcie bota?", default=False)

    # Lead sources
    LEAD_SOURCES = [
        (LeadSource.NOT_SPECIFIED, "Ogólnie zainteresowany"),
        (LeadSource.WEBINAR_PARTICIPANT, "Zgłoszenie - uczestnik webinaru"),
        (LeadSource.WEBINAR_CONTACT, "Zgłoszenie -  kontakt ogólny"),
        (LeadSource.NEWSLETTER_FOOTER, "Stopka - Zapis do newslettera"),
        (LeadSource.CONFERENCE_FREE, "Konferencja - uczestnik darmowy"),
        (LeadSource.CONFERENCE_PAID, "Konferencja - uczestnik płatny"),
        (LeadSource.EMAIL_MESSAGE_SIGNUP, "E-mail - poprosił od zapis przez e-mail"),
    ]

    lead_source = CharField(
        max_length=32,
        choices=LEAD_SOURCES,
        default=LeadSource.NOT_SPECIFIED,
        verbose_name="Źródło lead'a",
    )

    # Preferences
    preferences = ManyToManyField(
        "WebinarCategory",
        verbose_name="Kategorie",
        help_text="Jakimi kategoriami jest zainteresowany?",
        blank=True,
    )

    # Webinars
    webinars = ManyToManyField(
        "Webinar",
        verbose_name="Webinary",
        help_text="Na jakie webinary go zapisano?",
        blank=True,
    )

    # Conferences
    conferences = ManyToManyField(
        "ConferenceEdition",
        verbose_name="Konferencje",
        help_text="Na jakie konferencje się zapisał?",
        blank=True,
    )

    # Access tokens
    preferences_token = UUIDField("Token panelu preferencij", default=uuid.uuid4)
    unsubscribe_token = UUIDField("Token wypisu", default=uuid.uuid4)

    # Metadata
    singup_ip_address = CharField(max_length=64, blank=True)

    last_email_date = DateTimeField(
        null=True, blank=True, help_text="Ostatnio wysłana wiadomość e-mail"
    )
    last_email_opened = DateTimeField(
        null=True, blank=True, help_text="Ostatnio otwarto wiadomość e-mail"
    )
    last_email_clicked = DateTimeField(
        null=True, blank=True, help_text="Ostatnio kliknięto w wiadomość e-mail"
    )
    last_purchase_date = DateTimeField(
        null=True, blank=True, help_text="Ostatnio dokonano zakupu na stronie"
    )
    last_activity_date = DateTimeField(
        null=True, blank=True, help_text="Ostatnia jakaklowiek aktywność"
    )

    class Meta:
        verbose_name = "Lead (Główny)"
        verbose_name_plural = "Lead'y (Główne)"

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs) -> None:
        self.email = self.email.lower()
        return super().save(*args, **kwargs)
