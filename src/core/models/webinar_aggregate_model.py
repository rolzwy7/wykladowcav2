"""Webinar Aggregate"""

# flake8: noqa=E501

from django.db.models import (
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Manager,
    ManyToManyField,
    Model,
    Q,
    QuerySet,
    SlugField,
    TextField,
    URLField,
)
from django.utils.timezone import now, timedelta

from core.consts import SLUG_HELP_TEXT


class WebinarAggregateManager(Manager):
    """WebinarAggregate Manager"""

    def get_active_aggregates(self) -> QuerySet["WebinarAggregate"]:
        """get_active_aggregates"""
        return self.get_queryset().filter(
            Q(hidden=False)
            & Q(slug_conflict=False)
            & (Q(absolute_redirect="") | Q(parent=None))
            & ~Q(grouping_token="")
        )

    def get_active_aggregates_for_category_slugs(
        self, slugs: list[str]
    ) -> QuerySet["WebinarAggregate"]:
        """get_active_aggregates_for_category_slugs"""
        return (
            self.get_active_aggregates()
            .filter(categories__slug__in=slugs)
            .distinct()
            .order_by("closest_webinar_dt")
        )


class WebinarAggregate(Model):
    """WebinarAggregate"""

    manager = WebinarAggregateManager()

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    hidden = BooleanField("Ukryty", default=False)

    # PK
    grouping_token = CharField(
        "Token grupujący",
        max_length=32,
        primary_key=True,
        help_text="Ciąg znaków grupujący razem terminy",
    )

    slug = SlugField(
        "Skrót URL",
        max_length=230,
        unique=True,
        help_text=SLUG_HELP_TEXT,
    )

    # # SEO
    seo_meta_title = CharField("SEO Meta Title", max_length=70, blank=True)
    seo_meta_description = TextField("SEO Meta Description", max_length=160, blank=True)
    seo_canonical_url = URLField("SEO Canonical URL", blank=True)

    # meta_keywords = models.CharField(max_length=255, blank=True)
    # og_title = models.CharField(max_length=100, blank=True)
    # og_description = models.TextField(max_length=200, blank=True)
    # og_image = models.ImageField(upload_to='og_images/', blank=True)
    # twitter_title = models.CharField(max_length=70, blank=True)
    # twitter_description = models.TextField(max_length=200, blank=True)
    # twitter_image = models.ImageField(upload_to='twitter_images/', blank=True)
    # structured_data = models.JSONField(blank=True, null=True)
    # image_alt_text = models.CharField(max_length=125, blank=True)
    # h1_heading = models.CharField(max_length=100, blank=True)
    # published_date = models.DateTimeField(blank=True, null=True)
    # modified_date = models.DateTimeField(blank=True, null=True)
    # robots_meta = models.CharField(max_length=100, blank=True)

    # Automatic fill
    closest_webinar_dt = DateTimeField(null=True, blank=True)
    has_active_webinars = BooleanField("Ma aktywne webinary", default=False)

    # Conflicts
    slug_conflict = BooleanField("Slug conflict", default=False)
    title_conflict = BooleanField("Title conflict", default=False)
    program_conflict = BooleanField("Program conflict", default=False)
    program_assets_conflict = BooleanField(
        "Materiały szkoleniowe conflict", default=False
    )
    lecturer_conflict = BooleanField("Lecturer conflict", default=False)

    # Lecturer
    lecturer = ForeignKey(
        "Lecturer", on_delete=SET_NULL, blank=True, null=True, verbose_name="Wykładowca"
    )

    # Text
    title = TextField(
        "Tytuł szkolenia", max_length=220, blank=True, help_text="Max. 220 znaków"
    )
    short_description = TextField("Krótki opis", blank=True)
    program_assets = TextField("Materiały szkoleniowe", blank=True)
    program = TextField(
        "Program szkolenia", default="[Agregat Program Szkolenia]", blank=True
    )

    # Redirects
    absolute_redirect = CharField(max_length=32, blank=True)
    parent = ForeignKey(
        "WebinarAggregate",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        verbose_name="Rodzic",
    )

    # Nagranie na sprzedaz
    sale_recording = ForeignKey(
        "SaleRecording",
        null=True,
        blank=True,
        on_delete=SET_NULL,
        verbose_name="Nagranie na sprzedaż",
    )

    # Webinars
    webinars = ManyToManyField(
        "Webinar", verbose_name="Terminy", help_text="[Autouzupełnianie]", blank=True
    )

    # Categories
    categories = ManyToManyField(
        "WebinarCategory", verbose_name="Kategorie", blank=True
    )

    class Meta:
        verbose_name = "Agregat"
        verbose_name_plural = "Agregaty"

    @property
    def minimal_price(self):
        """minimal_price"""
        prices = [webinar.price for webinar in self.webinars.all() if webinar.is_active]
        if prices:
            return min(prices)
        else:
            return None

    @property
    def is_anonymized(self):
        """is_anonymized"""
        return any([webinar.is_lecturer_anonymized for webinar in self.webinars.all()])

    @property
    def is_new(self):
        """is_new"""
        return any(
            [
                now() < webinar.created_at + timedelta(days=3)
                for webinar in self.webinars.all()
            ]
        )

    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.grouping_token}"
