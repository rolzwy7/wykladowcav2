"""
Model representing custom site
"""

# flake8: noqa=E501
# pylint: disable=line-too-long

from django.db.models import (
    CharField,
    DateTimeField,
    Manager,
    Model,
    SlugField,
    TextField,
)


class CustomHtmlSiteManager(Manager):
    """Custom Html Site Manager"""

    ...


class CustomHtmlSite(Model):
    """Custom Html Site Model"""

    manager = CustomHtmlSiteManager()

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    title = CharField("Tytuł", max_length=250, blank=True)

    slug = SlugField(
        "Skrót URL",
        max_length=230,
        blank=False,
        unique=True,
        help_text="Ścieżka URL",
    )

    html = TextField("HTML")

    def __str__(self) -> str:
        return str(self.slug)

    class Meta:
        verbose_name = "Strona HTML"
        verbose_name_plural = "Strony HTML"

    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)
