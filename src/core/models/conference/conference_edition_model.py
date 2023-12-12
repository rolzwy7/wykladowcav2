# flake8: noqa

from django.db.models import (
    RESTRICT,
    CharField,
    DateTimeField,
    ForeignKey,
    Manager,
    Model,
    SlugField,
    TextField,
)

from core.utils.text import slugify


class ConferenceEditionManager(Manager):
    """ConferenceEditionManager"""

    ...


class ConferenceEdition(Model):
    """Represents CRM Company"""

    manager = ConferenceEditionManager()

    name = CharField("Nazwa edycji", max_length=230)

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

    date_from = DateTimeField("Data i Godzina (start)")
    date_to = DateTimeField("Data i Godzina (stop)")

    html = TextField("Treść HTML", blank=True)

    class Meta:
        verbose_name = "Konferencja (edycja)"
        verbose_name_plural = "Konferencje (edycja)"

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
