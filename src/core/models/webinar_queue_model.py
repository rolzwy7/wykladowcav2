"""Webinar Queue Model"""

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


class WebinarQueueManager(Manager):
    """Eventlog query Manager"""

    ...


class WebinarQueue(Model):
    """Metadat for Webinar model"""

    manager = WebinarQueueManager()

    created_at = DateTimeField(auto_now_add=True)

    # e-mail
    # tracking_code
    # aggregate
    # sent_email
    # ip address
    # user-agent

    class Meta:
        ordering = ["-created_at"]
