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

    ...


class Eventlog(Model):
    """Metadat for Webinar model"""

    manager = EventlogManager()

    created_at = DateTimeField(auto_now_add=True)

    kod_procedury = CharField("Kod procedury", max_length=64, primary_key=True)
    url = CharField("Url", max_length=256)

    class Meta:
        ordering = ["-created_at"]
