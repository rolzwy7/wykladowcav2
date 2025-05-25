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
)
from django.utils.timezone import now, timedelta

from core.consts import SLUG_HELP_TEXT


class WebinarAggregateManager(Manager):
    """WebinarAggregate Manager"""

    def get_active_aggregates(self) -> QuerySet["WebinarAggregate"]:
        """get_active_aggregates"""
        return self.get_queryset().filter(
            Q(slug_conflict=False)
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

    closest_webinar_dt = DateTimeField(null=True, blank=True)

    grouping_token = CharField(
        "Token grupujący",
        max_length=32,
        primary_key=True,
        help_text="Ciąg znaków grupujący razem terminy",
    )

    slug_conflict = BooleanField("Slug conflict", default=False)
    title_conflict = BooleanField("Title conflict", default=False)
    program_conflict = BooleanField("Program conflict", default=False)
    lecturer_conflict = BooleanField("Lecturer conflict", default=False)

    program = TextField(
        "Program szkolenia", default="[Agregat Program Szkolenia]", blank=True
    )
    short_description = TextField("Krótki opis", blank=True)
    lecturer = ForeignKey(
        "Lecturer", on_delete=SET_NULL, blank=True, null=True, verbose_name="Wykładowca"
    )

    has_active_webinars = BooleanField("Ma aktywne webinary", default=False)

    title = TextField(
        "Tytuł szkolenia",
        max_length=220,
        blank=True,
        help_text=(
            "Tytuł szkolenia zmodyfikowany,"
            " aby mieścił się w ogrniczonej ilości znaków"
        ),
    )

    absolute_redirect = CharField(max_length=32, blank=True)

    parent = ForeignKey(
        "WebinarAggregate",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        verbose_name="Rodzic",
    )

    slug = SlugField(
        "Skrót URL",
        max_length=230,
        unique=True,
        help_text=SLUG_HELP_TEXT,
    )

    webinars = ManyToManyField(
        "Webinar", verbose_name="Terminy", help_text="[Autouzupełnianie]", blank=True
    )

    # Categories
    categories = ManyToManyField(
        "WebinarCategory", verbose_name="Kategorie", blank=True
    )

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

    def __str__(self) -> str:
        return f"{self.grouping_token}"
