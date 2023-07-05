from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    Manager,
    Model,
    Q,
    QuerySet,
    TextField,
)
from django.utils.timezone import now


class EventlogManager(Manager):
    """Eventlog query Manager"""

    def todays_eventlogs(self) -> QuerySet["Eventlog"]:
        """Return all eventlogs from today"""
        _now = now()
        return self.get_queryset().filter(
            # Only show webinars with given status
            Q(created_at__year=_now.year)
            & Q(created_at__month=_now.month)
            & Q(created_at__day=_now.day)
        )

    def this_month_eventlogs(self) -> QuerySet["Eventlog"]:
        """Return all eventlogs from this month (skip current day)"""
        _now = now()
        return self.get_queryset().filter(
            # Only show webinars with given status
            Q(created_at__year=_now.year)
            & Q(created_at__month=_now.month)
            & ~Q(created_at__day=_now.day)
        )


class Eventlog(Model):
    """Metadat for Webinar model"""

    manager = EventlogManager()

    created_at = DateTimeField(auto_now_add=True)
    webinar = ForeignKey(
        "Webinar",
        on_delete=CASCADE,
        verbose_name="Webinar",
        null=True,
        blank=True,
    )
    application = ForeignKey(
        "WebinarApplication",
        on_delete=CASCADE,
        verbose_name="Zgłoszenie",
        null=True,
        blank=True,
    )
    participant = ForeignKey(
        "WebinarParticipant",
        on_delete=CASCADE,
        verbose_name="Uczestnik",
        null=True,
        blank=True,
    )
    title_html = TextField("Tytuł (HTML)")
    content_html = TextField("Treść (HTML)", blank=True)

    icon = CharField("Ikona", max_length=32, blank=True)
    color = CharField("Kolor", max_length=32, blank=True)

    class Meta:
        ordering = ["-created_at"]
