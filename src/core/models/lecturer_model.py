from django.conf import settings
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    EmailField,
    ImageField,
    Manager,
    ManyToManyField,
    Model,
    OneToOneField,
    QuerySet,
    SlugField,
)
from django_quill.fields import QuillField

from core.consts import SLUG_HELP_TEXT
from core.utils.text import slugify


class LecturerManager(Manager):
    """Lecturer query Manager"""

    def visible_on_page(self) -> QuerySet["Lecturer"]:
        """Returns lecturers that are visible on website page"""
        return self.get_queryset().filter(visible_on_page=True)


class Lecturer(Model):
    """This model represents Lecturer"""

    manager = LecturerManager()

    visible_on_page = BooleanField(
        "Widoczny na stronie",
        default=True,
        help_text="Czy wykładowca ma być widoczny na stronie",
    )

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
            "Obrazek powinien być dobrej jakości"
            "o wymiarach kwadratowych (np. 500px na 500px)"
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

    email = EmailField(
        "Adres E-mail", blank=True, help_text="E-mail kontaktowy do wykładowcy"
    )

    profession = CharField(
        "Profesja",
        max_length=40,
        blank=True,
        help_text="Widoczna na stronie webinaru pod imieniem i nazwiskiem",
    )

    class Meta:
        verbose_name = "Wykładowca"
        verbose_name_plural = "Wykładowcy"

    def __str__(self) -> str:
        return str(self.fullname)

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.fullname)
        return super().save(*args, **kwargs)
