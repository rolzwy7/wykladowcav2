from django.conf import settings
from django.db.models import (
    CASCADE,
    CharField,
    ImageField,
    ManyToManyField,
    Model,
    OneToOneField,
    SlugField,
)
from django_quill.fields import QuillField

from core.consts import SLUG_HELP_TEXT
from core.utils.text import slugify


class Lecturer(Model):
    class Meta:
        verbose_name = "Wykładowca"
        verbose_name_plural = "Wykładowcy"

    def __str__(self) -> str:
        return self.fullname

    fullname = CharField("Imie i Nazwisko", max_length=100)
    slug = SlugField(
        "Skrót URL", max_length=120, blank=False, help_text=SLUG_HELP_TEXT
    )

    categories = ManyToManyField("WebinarCategory", verbose_name="Kategorie")

    avatar = ImageField(
        "Avatar",
        blank=True,
        upload_to="uploads/lecturers",
        help_text=(
            "Obrazek powinien być dobrej jakości o wymiarach kwadratowych (np. 500px na 500px)"  # noqa
        ),
    )

    biography = QuillField("Biografia", blank=True)

    user = OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name="Użytkownik",
    )

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.fullname)
        return super().save(*args, **kwargs)
