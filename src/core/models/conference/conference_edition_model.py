"""
Conference edition model
"""

# flake8: noqa

import uuid

from django.db.models import (
    RESTRICT,
    SET_NULL,
    BooleanField,
    CharField,
    ForeignKey,
    Manager,
    Model,
    OneToOneField,
    QuerySet,
    SlugField,
    TextField,
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

    clickmeeting_id = CharField("ClickMeeting ID", blank=True, max_length=200)
    clickmeeting_url = CharField("ClickMeeting URL", blank=True, max_length=200)

    redirect_token = UUIDField(default=uuid.uuid4, editable=True)

    STREAM_TYPE = [
        ("FACEBOOK", "Facebook"),
        ("YOUTUBE", "YouTube"),
    ]

    clickmeeting_pasted = BooleanField("Dane strumienia przeklejone?", default=False)

    stream_url_page = CharField("Adres URL strony", blank=True, max_length=200)
    stream_url_embed = CharField("Adres Embed", blank=True, max_length=200)

    stream_type = CharField(
        "Gdzie stream?",
        max_length=16,
        choices=STREAM_TYPE,
        default="YOUTUBE",
    )

    stream_server_url = CharField("Adres URL serwera", blank=True, max_length=200)
    stream_transmission_key = CharField("Klucz strumienia", blank=True, max_length=200)

    dashboard_url = CharField("Adres URL dashboard", blank=True, max_length=200)

    advert_lecturer = ForeignKey(
        "Lecturer",
        on_delete=SET_NULL,
        verbose_name="Advert Wykładowca",
        null=True,
        blank=True,
    )
    advert_category = ForeignKey(
        "WebinarCategory",
        on_delete=SET_NULL,
        verbose_name="Advert Kategoria",
        null=True,
        blank=True,
    )

    advert_facebook_url = CharField("Advert FB URL", blank=True, max_length=200)
    advert_facebook_html = TextField("Advert FB HTML", blank=True)

    advert_webinar_url = CharField("Advert FB URL", blank=True, max_length=200)
    advert_webinar_html = TextField("Advert FB HTML", blank=True)

    chat = OneToOneField(
        "ConferenceChat", on_delete=SET_NULL, null=True, blank=True, verbose_name="Chat"
    )

    class Meta:
        """meta"""

        verbose_name = "Konferencja (edycja)"
        verbose_name_plural = "Konferencje (edycja)"

    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)
