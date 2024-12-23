"""
Conference cycle model
"""

# flake8: noqa=E501
# pylint: disable=line-too-long
# pylint: disable=missing-class-docstring

from django.db.models import (
    BooleanField,
    CharField,
    Manager,
    ManyToManyField,
    Model,
    SlugField,
    TextField,
)

from core.utils.text import slugify


class ConferenceCycleManager(Manager):
    """ConferenceCycleManager"""

    ...


class ConferenceCycle(Model):
    """Represents CRM Company"""

    manager = ConferenceCycleManager()

    visible_on_page = BooleanField("Widoczne na stronie", default=True)

    name = CharField("Nazwa cyklu", max_length=230)

    short_description = TextField(
        "Krótki opis", help_text="Krótki opis widoczny pod nazwą cyklu", blank=True
    )

    slug = SlugField(
        "Skrót URL",
        max_length=230,
        blank=True,
        unique=True,
        help_text="Slug (SEO)",
    )

    html = TextField("Treść HTML", blank=True)

    categories = ManyToManyField("WebinarCategory", verbose_name="Kategorie")

    facebook_image_url = CharField("Facebook image", max_length=250, blank=True)

    class Meta:
        verbose_name = "Konferencja (cykl)"
        verbose_name_plural = "Konferencje (cykl)"

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
