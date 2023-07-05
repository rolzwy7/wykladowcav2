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

from .enums import WebinarDuration, WebinarStatus


class WebinarManager(Manager):
    """Webinar query Manager"""

    def init_or_confirmed(self) -> QuerySet["Webinar"]:
        """Returns `initialized` of `confirmed` webinars

        Returns:
            QuerySet['Webinar']: queryset of webinars
        """
        return self.get_queryset().filter(
            # Only show webinars with given status
            Q(status__in=[WebinarStatus.INIT, WebinarStatus.CONFIRMED])
        )

    def done_or_canceled(self) -> QuerySet["Webinar"]:
        """Returns `done` of `canceled` webinars

        Returns:
            QuerySet['Webinar']: queryset of webinars
        """
        return self.get_queryset().filter(
            # Only show webinars with given status
            Q(status__in=[WebinarStatus.DONE, WebinarStatus.CANCELED])
        )

    def homepage_webinars(self) -> QuerySet["Webinar"]:
        """Returns webinars visible on homepage

        Returns:
            QuerySet['Webinar']: queryset of webinars
        """
        return self.init_or_confirmed().filter(
            # Show webinar on homepage N-15 minutes after the start
            date__gte=now()
            - timedelta(minutes=settings.WEBINAR_ARCHIVE_DELAY_MINUTES)
        )


class Webinar(Model):
    manager = WebinarManager()

    is_confirmed = BooleanField(
        "Pewny termin",
        default=False,
        help_text="Pokaż `Pewny termin` przy szkoleniu na stronie",  # noqa
    )
    remaining_places = PositiveSmallIntegerField(
        "Pozostało miejsc", default=0, blank=True
    )

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

    DURATION = [
        (WebinarDuration.H1_M00, "1 godzina"),
        (WebinarDuration.H1_M30, "1,5 godziny"),
        (WebinarDuration.H2_M00, "2 godziny"),
        (WebinarDuration.H2_M30, "2,5 godziny"),
        (WebinarDuration.H3_M00, "3 godziny"),
        (WebinarDuration.H3_M30, "3,5 godziny"),
        (WebinarDuration.H4_M00, "4 godziny"),
        (WebinarDuration.H4_M30, "4,5 godziny"),
        (WebinarDuration.H5_M00, "5 godzin"),
        (WebinarDuration.H5_M30, "5,5 godziny"),
        (WebinarDuration.H6_M00, "6 godzin"),
        (WebinarDuration.H6_M30, "6,5 godziny"),
        (WebinarDuration.H7_M00, "7 godzin"),
        (WebinarDuration.H7_M30, "7,5 godziny"),
        (WebinarDuration.H8_M00, "8 godzin"),
        (WebinarDuration.H8_M30, "8,5 godziny"),
        (WebinarDuration.H9_M00, "9 godzin"),
    ]

    # Date
    date = DateTimeField("Data i Godzina")
    duration = CharField(
        "Czas trwania",
        choices=DURATION,
        max_length=16,
        default=WebinarDuration.H4_M00,
    )

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

    @property
    def date_end(self):
        """Returns webinar's end datetime"""
        duration_minutes = int(self.duration)
        ret = self.date + timedelta(minutes=duration_minutes)
        return ret

    @property
    def is_discounted(self) -> bool:
        """Tells if webinar is discounted"""
        if self.discount_until:
            is_active = self.discount_until >= now()
            return is_active
        else:
            return False

    @property
    def price(self):
        """Resolves current NETTO price"""
        if self.is_discounted:
            return self.discount_netto
        else:
            return self.price_netto


class WebinarMetadata(Model):
    """Metadata for Webinar model"""

    webinar = OneToOneField("Webinar", on_delete=CASCADE)
    clickmeeting_id = CharField("ClickMeeting ID", blank=True, max_length=100)
    auto_send_invoices = BooleanField(
        "Automatyczne wysyłanie faktur",
        default=True,
        help_text="Czy po zrealizowanym szkoleniu faktury mają być wysłane automatycznie do wszystkich",  # noqa
    )

    lecturer_price_netto = PositiveSmallIntegerField(
        "Cena NETTO wykładowcy", default=0
    )

    def __str__(self) -> str:
        return f"Metadata for webinar {self.pk}"
