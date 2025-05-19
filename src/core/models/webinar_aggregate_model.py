"""Webinar Aggregate"""

# flake8: noqa=E501

from django.db.models import (
    SET_NULL,
    BooleanField,
    CharField,
    ForeignKey,
    Manager,
    ManyToManyField,
    Model,
    Q,
    QuerySet,
    SlugField,
    TextField,
)

from core.consts import SLUG_HELP_TEXT


class WebinarAggregateManager(Manager):
    """WebinarAggregate Manager"""

    def get_active_aggregates(self) -> QuerySet["WebinarAggregate"]:
        """get_active_aggregates"""
        return self.get_queryset().filter(
            Q(slug_conflict=False) & Q(title_conflict=False)
        )


class WebinarAggregate(Model):
    """WebinarAggregate"""

    manager = WebinarAggregateManager()

    grouping_token = CharField(
        "Token grupujący",
        max_length=32,
        primary_key=True,
        help_text="Ciąg znaków grupujący razem terminy",
    )

    slug_conflict = BooleanField("Slug conflict", default=False)
    title_conflict = BooleanField("Title conflict", default=False)

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

    def __str__(self) -> str:
        return f"{self.grouping_token}"
