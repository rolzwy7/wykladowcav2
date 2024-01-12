"""
Conference edition model
"""

# flake8: noqa

from django.db.models import (
    RESTRICT,
    CharField,
    DateTimeField,
    ForeignKey,
    Manager,
    ManyToManyField,
    Model,
    QuerySet,
    SlugField,
    TextField,
)

from core.utils.text import slugify

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

    name = CharField("Nazwa edycji", max_length=230)

    title = CharField("Tytuł edycji", max_length=230, blank=True)

    slug = SlugField(
        "Skrót URL",
        max_length=230,
        blank=True,
        unique=True,
        help_text="Slug (SEO)",
    )

    cycle = ForeignKey(
        "ConferenceCycle", on_delete=RESTRICT, verbose_name="Konferencja (cykl)"
    )

    webinar = ForeignKey(
        "Webinar",
        on_delete=RESTRICT,
        verbose_name="Webinar (płatny dostęp)",
        null=True,
        blank=True,
    )

    categories = ManyToManyField("WebinarCategory", verbose_name="Kategorie")

    date_from = DateTimeField("Data i Godzina (start)")
    date_to = DateTimeField("Data i Godzina (stop)")

    html = TextField("Treść HTML", blank=True)

    clickmeeting_id = CharField("ClickMeeting ID", blank=True, max_length=100)

    youtube_live_embed = TextField("YouTube Livestream Embed", blank=True)

    class Meta:
        verbose_name = "Konferencja (edycja)"
        verbose_name_plural = "Konferencje (edycja)"

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
