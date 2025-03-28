# flake8: noqa:E501
# pylint: disable=line-too-long
from django.conf import settings
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
    ImageField,
    Manager,
    ManyToManyField,
    Model,
    OneToOneField,
    PositiveIntegerField,
    Q,
    QuerySet,
    SlugField,
    TextField,
)
from django.urls import reverse

from core.consts import SLUG_HELP_TEXT
from core.utils.text import slugify

BASE_URL = settings.BASE_URL


class LecturerManager(Manager):
    """Lecturer query Manager"""

    def get_allowed_to_display_lecturers(self) -> QuerySet["Lecturer"]:
        """Returns lecturers that are allowed to be displayed"""
        return self.get_queryset().filter(Q(finished_coop=False) & Q(anonymize=False))

    def get_lecturers_visible_on_page(self) -> QuerySet["Lecturer"]:
        """Returns lecturers that are visible on website"""
        return self.get_allowed_to_display_lecturers().filter(visible_on_page=True)

    def get_lecturers_visible_on_homepage(self) -> QuerySet["Lecturer"]:
        """Returns lecturers that are visible on homepage"""
        return self.get_allowed_to_display_lecturers().filter(
            Q(visible_on_page=True) & Q(visible_on_homepage=True)
        )


class Lecturer(Model):
    """This model represents Lecturer"""

    manager = LecturerManager()

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    visible_on_page = BooleanField(
        "Widoczny na stronie",
        default=True,
        help_text="Czy wykładowca ma być widoczny na stronie",
    )

    visible_on_homepage = BooleanField(
        "Widoczny na stronie głównej",
        default=False,
        help_text="Czy wykładowca ma być widoczny na stronie głównej",
    )

    agrees_to_recording = BooleanField(
        "Zgadza się na nagrania",
        default=True,
        help_text="Czy wykładowca zgadza się na nagrania",
    )

    finished_coop = BooleanField(
        "Zakończono współpracę",
        default=False,
        help_text="Wykładowca nie chce mieć z nami nic wspólnego",
    )

    forbid_mailing_alias = BooleanField(
        "Nie chce być w Aliasie w mailingu",
        default=False,
        help_text="Wykładowca nie chce być widoczny z imienia i nazwiska w aliasie w mailingu",
    )

    anonymize = BooleanField(
        "Anonimizuj wykładowcę",
        default=False,
        help_text="Wykładowca będzie zanonimizowany",
    )

    order_value = PositiveIntegerField("Wartość sortująca", default=100)

    fullname = CharField("Imie i Nazwisko", max_length=100)

    slug = SlugField("Skrót URL", max_length=120, blank=False, help_text=SLUG_HELP_TEXT)

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

    biography = TextField("Biografia", blank=True)

    biography_email = TextField("Biografia (e-mail)", blank=True)

    very_short_biography = TextField("Bardzo krótka biografia", blank=True)

    biography_anonymous = TextField("Biografia (anonim)", blank=True)

    notes = TextField("Notatki", blank=True, help_text="Widoczne tylko tutaj w CMS")

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

    fake_stat_participants = PositiveIntegerField("Przeszkolonych (baza)", default=0)
    fake_stat_webinars = PositiveIntegerField(
        "Przeprowadzonych szkoleń (baza)", default=0
    )
    years_experience = CharField(
        "Lata doświadczenia",
        max_length=40,
        blank=True,
        help_text="np. `5 lat`",
    )

    class Meta:
        verbose_name = "Wykładowca"
        verbose_name_plural = "Wykładowcy"

    def __str__(self) -> str:
        return str(self.fullname)

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.fullname)
        return super().save(*args, **kwargs)

    @property
    def opinion_absolute_url(self):
        """opinion_absolute_url"""
        return settings.BASE_URL + reverse(
            "core:lecturer_opinion_form_page", kwargs={"slug": self.slug}
        )
