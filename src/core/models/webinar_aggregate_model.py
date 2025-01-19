"""Webinar Aggregate"""

from django.db.models import CharField, Manager, Model, QuerySet, SlugField

from core.consts import SLUG_HELP_TEXT
from core.models.enums import WebinarAggregateStatus


class WebinarAggregateManager(Manager):
    """WebinarAggregate Manager"""

    def get_published_aggregates(self) -> QuerySet["WebinarAggregate"]:
        """Returns `done` webinars

        Returns:
            QuerySet['Webinar']: queryset of webinars
        """
        return self.get_queryset().filter(
            # Only show webinars with given status
            status=WebinarAggregateStatus.PUBLISHED
        )


class WebinarAggregate(Model):
    """WebinarAggregate"""

    manager = WebinarAggregateManager()

    STATUS = [
        (WebinarAggregateStatus.DRAFT, "Wersja robocza"),
        (WebinarAggregateStatus.PUBLISHED, "Opublikowany"),
        (WebinarAggregateStatus.REJECTED, "Odrzucony"),
    ]

    status = CharField(
        max_length=32, default=WebinarAggregateStatus.DRAFT, choices=STATUS
    )

    slug = SlugField(
        "Skrót URL",
        max_length=230,
        unique=True,
        help_text=SLUG_HELP_TEXT,
    )

    grouping_token = CharField(
        "Token grupujący",
        max_length=32,
        primary_key=True,
        help_text="Ciąg znaków grupujący razem terminy",
    )

    def __str__(self) -> str:
        return f"gt-{self.grouping_token}"
