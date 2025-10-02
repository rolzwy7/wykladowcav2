"""Webinar Queue Model"""

# flake8: noqa=E501
import uuid

from django.db.models import (
    RESTRICT,
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
    ForeignKey,
    Manager,
    Model,
    UUIDField,
)


class WebinarQueueManager(Manager):
    """Eventlog query Manager"""

    ...


class WebinarQueue(Model):
    """Metadat for Webinar model"""

    manager = WebinarQueueManager()

    created_at = DateTimeField(auto_now_add=True)

    # Basic info
    email = EmailField("Adres E-mail")

    phone = CharField("Telefon", max_length=32, blank=True)

    aggregate = ForeignKey(
        "WebinarAggregate",
        on_delete=RESTRICT,
        verbose_name="Agregat",
    )
    aggregate_current_title = CharField(max_length=256, blank=True)

    # Tracking info
    spy_object = ForeignKey(
        "SpyObject",
        on_delete=RESTRICT,
        null=True,
        blank=True,
        verbose_name="Spy Object",
    )

    # Notification
    sent_notification = BooleanField("Wysłano e-mail?", default=False)
    sent_notification_at = DateTimeField("Kiedy wysłano e-mail", null=True, blank=True)

    @property
    def domain(self):
        """get email's domain"""
        return self.email.split("@")[1]

    class Meta:
        ordering = ["-created_at"]
