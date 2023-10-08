import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
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
    PositiveIntegerField,
    PositiveSmallIntegerField,
    Q,
    QuerySet,
    SlugField,
    TextField,
    URLField,
    UUIDField,
)
from django.template.defaultfilters import timeuntil_filter
from django.utils.timezone import now, timedelta

from core.consts import SLUG_HELP_TEXT

from .enums import WebinarDuration, WebinarStatus


class WebinarManager(Manager):
    """Webinar query Manager"""

    def get_init_or_confirmed_webinars(self) -> QuerySet["Webinar"]:
        """Returns `initialized` of `confirmed` webinars

        Returns:
            QuerySet['Webinar']: queryset of webinars
        """
        return self.get_queryset().filter(
            # Only show webinars with given status
            Q(status__in=[WebinarStatus.INIT, WebinarStatus.CONFIRMED])
        )

    def get_done_or_canceled_webinars(self) -> QuerySet["Webinar"]:
        """Returns `done` of `canceled` webinars

        Returns:
            QuerySet['Webinar']: queryset of webinars
        """
        return self.get_queryset().filter(
            # Only show webinars with given status
            Q(status__in=[WebinarStatus.DONE, WebinarStatus.CANCELED])
        )

    def get_active_webinars(self) -> QuerySet["Webinar"]:
        """Returns active webinars

        Returns:
            QuerySet['Webinar']: queryset of webinars
        """
        return (
            self.get_init_or_confirmed_webinars()
            .filter(
                # Show webinar on homepage N-15 minutes after the start
                date__gte=now()
                - timedelta(minutes=settings.WEBINAR_ARCHIVE_DELAY_MINUTES)
            )
            .order_by("date")
        )

    def get_active_webinars_for_category(
        self, slug: str
    ) -> QuerySet["Webinar"]:
        """Returns webinars for given category slug

        Returns:
            QuerySet['Webinar']: queryset of webinars
        """
        return self.get_active_webinars().filter(categories__slug__in=[slug])

    def get_active_webinars_for_lecturer(
        self, lecturer_id: int
    ) -> QuerySet["Webinar"]:
        """Returns webinars for given lecturer id

        Returns:
            QuerySet['Webinar']: queryset of webinars
        """
        return self.get_active_webinars().filter(lecturer__id=lecturer_id)


class Webinar(Model):
    """Represents webinar"""

    manager = WebinarManager()

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    is_confirmed = BooleanField(
        "Pewny termin",
        default=False,
        help_text="Pokaż `Pewny termin` przy szkoleniu na stronie",  # noqa
    )

    recording_allowed = BooleanField(
        "Nagrania dostępne",
        default=False,
        help_text="Wykładowca zgadza się na nagranie z tego szkolenia",  # noqa
    )

    remaining_places = PositiveSmallIntegerField(
        "Pozostało miejsc", default=0, blank=True
    )

    STATUS = [
        (WebinarStatus.INIT, "Planowany termin"),
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
        help_text=(
            "Tytuł szkolenia zmodyfikowany,"
            " aby mieścił się w ogrniczonej ilości znaków"
        ),
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
    categories = ManyToManyField(
        "WebinarCategory", verbose_name="Kategorie", blank=True
    )

    # Program
    program = TextField("Program szkolenia", default="[Program Szkolenia]")
    program_markdown = TextField("Program szkolenia (markdown)", blank=True)
    program_enchanted = TextField("Program szkolenia (enchanted)", blank=True)

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
        return super().save(*args, **kwargs)

    @property
    def date_end(self):
        """Returns webinar's end datetime"""
        duration_minutes = int(self.duration)
        ret = self.date + timedelta(minutes=duration_minutes)
        return ret

    @property
    def time_to_webinar(self) -> str:
        """Returns formatted time left to webinar or False
        if webinar start date is in the past
        """
        return (
            "" if now() > self.date else timeuntil_filter(self.date, arg=now())
        )

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

    @property
    def discount_value(self):
        """Discount NETTO value"""
        return self.price_netto - self.discount_netto

    def clean(self):
        # Make sure that discount price is >= than normal price
        if all(
            [
                self.discount_netto is not None,
                self.price_netto is not None,
                self.discount_netto >= self.price_netto,
            ]
        ):
            raise ValidationError(
                "Cena promocyjna nie może być większa niż normalna cena"
            )


class WebinarMetadata(Model):
    """Metadata for Webinar model"""

    webinar = OneToOneField("Webinar", on_delete=CASCADE)
    clickmeeting_id = CharField("ClickMeeting ID", blank=True, max_length=100)
    auto_send_invoices = BooleanField(
        "Automatyczne wysyłanie faktur",
        default=True,
        help_text=(
            "Czy po zrealizowanym szkoleniu faktury mają być wysłane"
            " automatycznie do wszystkich"
        ),
    )

    lecturer_price_netto = PositiveSmallIntegerField(
        "Cena NETTO wykładowcy", default=0
    )

    assets_token = UUIDField("Token dostępu do materiałów", default=uuid.uuid4)

    click_count_mailing = PositiveIntegerField("Kliknięcia Mailing", default=0)
    click_count_facebook = PositiveIntegerField(
        "Kliknięcia Facebook", default=0
    )
    site_enter_count = PositiveIntegerField("Wejść na stronę", default=0)

    def __str__(self) -> str:
        return f"Metadata for webinar {self.pk}"
