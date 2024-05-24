"""
Conference edition model
"""

# flake8: noqa

import uuid

from django.db.models import (
    RESTRICT,
    CharField,
    ForeignKey,
    Manager,
    Model,
    OneToOneField,
    QuerySet,
    SlugField,
    UUIDField,
)

from .conference_cycle_model import ConferenceCycle


class ConferenceEditionManager(Manager):
    """ConferenceEditionManager"""

    def get_active_editions_for_cycle(
        self, cycle: ConferenceCycle
    ) -> QuerySet["ConferenceEdition"]:
        """Get visible categories"""
        return self.get_queryset().filter(cycle=cycle)


class ConferenceEdition(Model):
    """Represents CRM Company"""

    manager = ConferenceEditionManager()

    slug = SlugField(
        "Skrót URL",
        max_length=230,
        blank=True,
        unique=True,
        help_text="Slug (SEO)",
    )

    cycle = ForeignKey(
        "ConferenceCycle",
        blank=True,
        null=True,
        on_delete=RESTRICT,
        verbose_name="Konferencja (cykl)",
    )

    webinar = OneToOneField(
        "Webinar",
        on_delete=RESTRICT,
        verbose_name="Webinar",
    )

    clickmeeting_id = CharField("ClickMeeting ID", max_length=200)
    clickmeeting_url = CharField("ClickMeeting URL", max_length=200)

    redirect_token = UUIDField(default=uuid.uuid4, editable=True)

    STREAM_TYPE = [
        ("FACEBOOK", "Facebook"),
        ("YOUTUBE", "YouTube"),
    ]

    stream_url = CharField("Adres URL strumienia", blank=True, max_length=200)

    stream_type = CharField(
        "Gdzie stream?",
        max_length=16,
        choices=STREAM_TYPE,
        default="YOUTUBE",
    )

    stream_url_address = CharField("Adres URL serwera", blank=True, max_length=200)
    stream_transmission_key = CharField("Klucz strumienia", blank=True, max_length=200)

    class Meta:
        """meta"""

        verbose_name = "Konferencja (edycja)"
        verbose_name_plural = "Konferencje (edycja)"

    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)
