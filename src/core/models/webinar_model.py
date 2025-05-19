# flake8: noqa=E501


import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import (
    CASCADE,
    RESTRICT,
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    ImageField,
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
from django.template.defaultfilters import date as _date
from django.template.defaultfilters import timeuntil_filter
from django.utils.timezone import now, timedelta
from simple_history.models import HistoricalRecords

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

    def get_init_or_confirmed_or_draft_webinars(self) -> QuerySet["Webinar"]:
        """Returns `initialized` of `confirmed` or `draft` webinars

        Returns:
            QuerySet['Webinar']: queryset of webinars
        """
        return self.get_queryset().filter(
            # Only show webinars with given status
            Q(
                status__in=[
                    WebinarStatus.INIT,
                    WebinarStatus.CONFIRMED,
                    WebinarStatus.DRAFT,
                ]
            )
        )

    def get_draft_webinars(self) -> QuerySet["Webinar"]:
        """Returns `draft` webinars

        Returns:
            QuerySet['Webinar']: queryset of webinars
        """
        return self.get_queryset().filter(
            # Only show webinars with given status
            Q(status__in=[WebinarStatus.DRAFT])
        )

    def get_done_or_canceled_webinars(self) -> QuerySet["Webinar"]:
        """Returns `done` or `canceled` webinars

        Returns:
            QuerySet['Webinar']: queryset of webinars
        """
        return self.get_queryset().filter(
            # Only show webinars with given status
            Q(status__in=[WebinarStatus.DONE, WebinarStatus.CANCELED])
        )

    def get_done_webinars(self) -> QuerySet["Webinar"]:
        """Returns `done` webinars

        Returns:
            QuerySet['Webinar']: queryset of webinars
        """
        return self.get_queryset().filter(
            # Only show webinars with given status
            status=WebinarStatus.DONE
        )

    def get_canceled_webinars(self) -> QuerySet["Webinar"]:
        """Returns `canceled` webinars

        Returns:
            QuerySet['Webinar']: queryset of webinars
        """
        return self.get_queryset().filter(
            # Only show webinars with given status
            Q(status=WebinarStatus.CANCELED)
        )

    def get_visible_webinars(self) -> QuerySet["Webinar"]:
        """Get visible webinars"""
        return self.get_queryset().filter(is_hidden=False)

    def get_active_webinars(self) -> QuerySet["Webinar"]:
        """Returns active webinars

        Returns:
            QuerySet['Webinar']: queryset of webinars
        """
        return (
            self.get_init_or_confirmed_webinars()
            .filter(
                Q(is_hidden=False)
                &
                # Show webinar on homepage N-15 minutes after the start
                Q(
                    date__gte=now()
                    - timedelta(minutes=settings.WEBINAR_ARCHIVE_DELAY_MINUTES)
                )
            )
            .order_by("date")
        )

    def get_archived_webinars(self) -> QuerySet["Webinar"]:
        """Returns archived webinars

        Returns:
            QuerySet['Webinar']: queryset of webinars
        """
        return (
            self.get_done_or_canceled_webinars()
            .filter(is_hidden=False)
            .order_by("date")
        )

    def get_active_webinars_for_category_slugs(
        self, slugs: list[str]
    ) -> QuerySet["Webinar"]:
        """Returns webinars for given category slugs

        Returns:
            QuerySet['Webinar']: queryset of webinars
        """
        return (
            self.get_active_webinars()
            .filter(
                # Parent's slug
                Q(categories__slug__in=slugs)
                # Grandparent's slug
                | Q(categories__parent__slug__in=slugs)
            )
            .distinct()
        )

    def get_archived_webinars_for_category_slugs(
        self, slugs: list[str]
    ) -> QuerySet["Webinar"]:
        """Returns archived webinars for given category slugs

        Returns:
            QuerySet['Webinar']: queryset of webinars
        """
        return (
            self.get_archived_webinars()
            .filter(
                # Parent's slug
                Q(categories__slug__in=slugs)
                # Grandparent's slug
                | Q(categories__parent__slug__in=slugs)
            )
            .distinct()
        )

    def get_active_webinars_for_lecturer(self, lecturer_id: int) -> QuerySet["Webinar"]:
        """Returns webinars for given lecturer id

        Returns:
            QuerySet['Webinar']: queryset of webinars
        """
        return self.get_active_webinars().filter(lecturer__id=lecturer_id)

    def get_active_conferences(self) -> QuerySet["Webinar"]:
        """Get active conferences

        Returns:
            QuerySet['Webinar']: queryset of conferences
        """
        return self.get_active_webinars().filter(is_connected_to_conference=True)


class Webinar(Model):
    """Represents webinar"""

    manager = WebinarManager()
    history = HistoricalRecords()

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    webinar_aggregate = ForeignKey(
        "WebinarAggregate",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        verbose_name="Agregat",
        help_text="(Samo się wypełni) Agregat grupujący terminy webinarów",
    )

    fakturownia_category = ForeignKey(
        "FakturowniaCategory",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        verbose_name="Kategoria Fakturownia",
    )

    is_confirmed = BooleanField(
        "Pewny termin",
        default=False,
        help_text="Pokaż `Pewny termin` przy szkoleniu na stronie",  # noqa
    )

    is_fake = BooleanField("Fake'owy termin", default=False)

    show_lecturer = BooleanField("Pokaż wykładowce na stronie szkolenia", default=True)

    anonymize_lecturer = BooleanField(
        "Anonimizuj wykładowcę",
        default=False,
        help_text="Wykładowca będzie zanonimizowany",
    )

    is_hidden = BooleanField(
        "Ukryj termin szkolenia na stronie",
        default=False,
        help_text="Nie będzie można wyszukać terminu, ale będzie można wejść bezpośrednio",
    )

    is_connected_to_conference = BooleanField(
        "Połączony z konferencją",
        default=False,
        help_text="Czy ten webinar jest połączony z konferencją?",  # noqa
    )

    recording_allowed = BooleanField(
        "Nagrania dostępne",
        default=False,
        help_text="Wykładowca zgadza się na nagranie z tego szkolenia",  # noqa
    )

    remaining_places = PositiveSmallIntegerField(
        "Pozostało miejsc", default=10, blank=True
    )

    STATUS = [
        (WebinarStatus.DRAFT, "Wersja robocza"),
        (WebinarStatus.INIT, "Planowany termin"),
        (WebinarStatus.CONFIRMED, "Termin potwierdzony"),
        (WebinarStatus.CANCELED, "Termin odwołany"),
        (WebinarStatus.DONE, "Termin zrealizowany"),
    ]

    status = CharField(max_length=32, default=WebinarStatus.INIT, choices=STATUS)

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
        "Skrót URL",
        max_length=230,
        blank=True,
        unique=True,
        help_text=SLUG_HELP_TEXT,
    )

    # Description
    description = TextField(
        "Dodatkowy opis",
        max_length=200,
        blank=True,
        help_text="Dodatkowy opis webinaru",
    )

    DURATION = [
        (WebinarDuration.H0_M30, "30 minut"),
        (WebinarDuration.H0_M45, "45 minut"),
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
        "Cena NETTO (Promocyjna)", default=0, blank=True, null=True
    )
    discount_until = DateTimeField("Promocja do", blank=True, null=True)

    # Lecturer
    lecturer = ForeignKey("Lecturer", on_delete=CASCADE, verbose_name="Wykładowca")

    # Categories
    categories = ManyToManyField(
        "WebinarCategory", verbose_name="Kategorie", blank=True
    )

    # Program
    program_assets = TextField("Materiały szkoleniowe", blank=True)
    program = TextField("Program szkolenia", default="[Program Szkolenia]")
    program_markdown = TextField("Program szkolenia (markdown)", blank=True)
    program_pretty = TextField("Program szkolenia (enchanted)", blank=True)
    program_short = TextField("Program szkolenia (krótki)", blank=True)
    program_word_text = TextField("Program (Word Text)", blank=True)

    # External
    external_name = CharField("Zewnętrzny dostawca - Nazwa", max_length=64, blank=True)
    external_url = URLField("Zewnętrzny dostawca - URL", blank=True)
    external_description = TextField("Zewnętrzny dostawca - Opis", blank=True)

    # Nagranie na sprzedaz
    sale_recording = ForeignKey(
        "SaleRecording",
        null=True,
        blank=True,
        on_delete=SET_NULL,
        verbose_name="Nagranie na sprzedaż",
    )

    # Grouping
    grouping_token = CharField(
        "Token grupujący",
        max_length=32,
        blank=True,
        help_text="Ciąg znaków grupujący razem terminy",
    )

    facebook_post_image = ImageField(
        "Facebook Post Image",
        blank=True,
        upload_to="uploads/webinar-facebook-covers",
        help_text=("wymiary: 1200px na 630px"),
    )

    seo_webinar_redirect = ForeignKey(
        "Webinar",
        on_delete=RESTRICT,
        null=True,
        blank=True,
        verbose_name="SEO Webinar Redirect",
    )

    seo_manual_redirect = CharField(
        "SEO Manual Redirect",
        max_length=512,
        blank=True,
        help_text="SEO Manual Redirect",
    )

    class Meta:
        verbose_name = "Webinar"
        verbose_name_plural = "Webinary"
        ordering = ["date"]

    def __str__(self) -> str:
        return f"({_date(self.date, 'j E Y')}) {self.title}"

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
        return "" if now() > self.date else timeuntil_filter(self.date, arg=now())

    @property
    def is_discounted(self) -> bool:
        """Tells if webinar is discounted"""
        if self.discount_until:
            return self.discount_until >= now()
        else:
            return False

    @property
    def price(self):
        """Resolves current NETTO price"""
        if self.is_discounted and self.discount_netto:
            return self.discount_netto
        else:
            return self.price_netto

    @property
    def discount_value(self):
        """Discount NETTO value"""
        if self.discount_netto:
            return self.price_netto - self.discount_netto
        else:
            return 0

    @property
    def is_archival(self):
        """Is webinar archival"""
        return any(
            [
                self.status in [WebinarStatus.DONE, WebinarStatus.CANCELED],
                now() > self.date + timedelta(days=3),
            ]
        )

    @property
    def human_date(self):
        """Display webinar datetime in human format"""
        return _date(self.date, "j E Y - H:i")

    @property
    def is_default_program(self):
        """Check if default program is set"""
        return any(
            [
                "[program szkolenia]" in str(self.program).lower(),
                self.program == "",
                len(self.program) < 50,
            ]
        )

    @property
    def is_lecturer_anonymized(self):
        """Check if lecturer is anonymized"""
        return self.anonymize_lecturer or self.lecturer.anonymize

    def clean(self):

        try:
            self.lecturer
        except Exception as e:
            raise ValidationError("Nie podano wykładowcy") from e

        # Make sure that discount price is >= than normal price
        if all(
            [
                self.price_netto is not None,
                self.discount_netto and self.discount_netto >= self.price_netto,
            ]
        ):
            raise ValidationError(
                "Cena promocyjna nie może być większa niż normalna cena"
            )

        # Make sure that lecturer agrees to recordings
        if self.lecturer and (
            not self.lecturer.agrees_to_recording and self.recording_allowed
        ):
            raise ValidationError(
                f"Wykładowca `{self.lecturer.fullname}` nie zgadza się na nagrania"
            )

        # Make sure that when `discount_netto` is set `discount_until` must be too
        if self.discount_netto is None and self.discount_until:
            raise ValidationError(
                "`Promocja do` nie może być ustawiona bez `Cena NETTO (Promocyjna)`"
            )
        if self.discount_until is None and self.discount_netto:
            raise ValidationError(
                "`Cena NETTO (Promocyjna)` nie może być ustawiona bez `Promocja do`"
            )


class WebinarMetadata(Model):
    """Metadata for Webinar model"""

    webinar = OneToOneField("Webinar", on_delete=CASCADE)
    clickmeeting_id = CharField("ClickMeeting ID", blank=True, max_length=100)

    lecturer_price_netto = PositiveSmallIntegerField("Cena NETTO wykładowcy", default=0)

    assets_token = UUIDField("Token dostępu do materiałów", default=uuid.uuid4)

    click_count_onesignal = PositiveIntegerField("Kliknięcia Onesignal", default=0)
    click_count_mailing = PositiveIntegerField("Kliknięcia Mailing", default=0)
    click_count_facebook = PositiveIntegerField("Kliknięcia Facebook", default=0)
    site_enter_count = PositiveIntegerField("Wejść na stronę", default=0)

    fetched_from = CharField("fetched_from", blank=True, max_length=32)
    fetched_from_url = CharField("fetched_from_url", blank=True, max_length=512)
    fetched_too_long_title = BooleanField("fetched_too_long_title", default=False)

    omega_indexer_queued = BooleanField("omega_indexer_queued", default=False)

    mailing_dobijanie_enabled = BooleanField("mailing_dobijanie_enabled", default=False)

    def __str__(self) -> str:
        return f"Metadata for webinar {self.pk}"
