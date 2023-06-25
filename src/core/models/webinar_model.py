from django.conf import settings
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Manager,
    ManyToManyField,
    Model,
    OneToOneField,
    PositiveSmallIntegerField,
    Q,
    QuerySet,
    SlugField,
    TextField,
    URLField,
)
from django.utils.timezone import now, timedelta
from django_quill.fields import QuillField

from core.consts import SLUG_HELP_TEXT
from core.utils.text import slugify

from .enums import WebinarStatus


class WebinarManager(Manager):
    """Webinar query Manager"""

    def homepage_webinars(self) -> QuerySet["Webinar"]:
        """Returns webinars visible on homepage

        Returns:
            QuerySet['Webinar']: queryset of webinars
        """
        return self.get_queryset().filter(
            # Only show webinars with given status
            Q(status__in=[WebinarStatus.INIT, WebinarStatus.CONFIRMED])
            # Show webinar on homepage N-15 minutes after the start
            & Q(
                date__gte=now()
                - timedelta(minutes=settings.WEBINAR_ARCHIVE_DELAY_MINUTES)
            )
        )


class Webinar(Model):
    manager = WebinarManager()

    STATUS = [
        (WebinarStatus.INIT, "Termin wystawiony"),
        (WebinarStatus.CONFIRMED, "Termin potwierdzony"),
        (WebinarStatus.CANCELED, "Termin odwołany"),
        (WebinarStatus.DONE, "Termin zrealizowany"),
    ]

    status = CharField(
        max_length=32, default=WebinarStatus.INIT, choices=STATUS
    )

    # Title
    title_original = TextField(
        "Pełny tytuł szkolenia",
        help_text="Tytuł szkolenia jaki został dostarczony przez wykładowce",
    )
    title = TextField(
        "Tytuł szkolenia",
        max_length=220,
        help_text="Tytuł szkolenia zmodyfikowany, aby mieścił się w ogrniczonej ilości znaków",  # noqa
    )
    slug = SlugField(
        "Skrót URL", max_length=230, unique=True, help_text=SLUG_HELP_TEXT
    )

    # Description
    description = TextField(
        "Dodatkowy opis",
        max_length=200,
        blank=True,
        help_text="Dodatkowy opis webinaru",
    )

    # Date
    date = DateTimeField("Data i Godzina")

    # Price
    price_netto = PositiveSmallIntegerField("Cena NETTO")
    discount_netto = PositiveSmallIntegerField(
        "Cena NETTO (Promocyjna)", default=0
    )
    discount_until = DateTimeField("Promocja do", blank=True, null=True)

    # Lecturer
    lecturer = ForeignKey(
        "Lecturer", on_delete=CASCADE, verbose_name="Wykładowca"
    )

    # Categories
    categories = ManyToManyField("WebinarCategory", verbose_name="Kategorie")

    # Program
    program = QuillField("Program szkolenia", default="[Program Szkolenia]")

    # External
    external_name = CharField(
        "Zewnętrzny dostawca - Nazwa", max_length=64, blank=True
    )
    external_url = URLField("Zewnętrzny dostawca - URL", blank=True)
    external_description = TextField("Zewnętrzny dostawca - Opis", blank=True)

    class Meta:
        verbose_name = "Webinar"
        verbose_name_plural = "Webinary"
        ordering = ["date"]

    def __str__(self) -> str:
        return str(self.title)

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class WebinarMetadata(Model):
    webinar = OneToOneField("Webinar", on_delete=CASCADE)
    clickmeeting_id = CharField("ClickMeeting ID", blank=True, max_length=100)
    auto_send_invoices = BooleanField(
        "Automatyczne wysyłanie faktur",
        default=True,
        help_text="Czy po zrealizowanym szkoleniu faktury mają być wysłane automatycznie do wszystkich",  # noqa
    )
    is_confirmed = BooleanField(
        "Termin potwierdzony",
        default=False,
        help_text="Oznacza termin jako `Termin potwierdzony` na stronie. To czysto kosmetyczna funckja.",  # noqa
    )
    remaining_places = PositiveSmallIntegerField(
        "Pozostało miejsc", default=0, blank=True
    )
