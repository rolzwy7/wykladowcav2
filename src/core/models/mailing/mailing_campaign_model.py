from datetime import time
from random import choices

from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Manager,
    Model,
    Q,
    QuerySet,
    TextField,
    TimeField,
)
from django.utils.timezone import now

from core.models.enums import MailingCampaignStatus


def default_allowed_to_send_after():
    """Default `allowed to send after` time"""
    return time(7, 30, 0, 0)


def default_allowed_to_send_before():
    """Default `allowed to send before` time"""
    return time(16, 0, 0, 0)


class MailingCampaignManager(Manager):
    """Mailing campaign manager"""

    def active_campaigns(self) -> QuerySet["MailingCampaign"]:
        """Returns active mailing campaigns"""
        return self.get_queryset().filter(
            Q(status=MailingCampaignStatus.SENDING)
            & Q(allowed_to_send_after__lt=now())
            & Q(allowed_to_send_before__gt=now())
        )


class MailingCampaign(Model):
    """Represents mailing campaign"""

    manager = MailingCampaignManager()

    created_at = DateTimeField(auto_now_add=True)
    title = CharField("Tytuł kampanii", max_length=100)

    # Sender
    smtp_sender = ForeignKey(
        "SmtpSender", on_delete=CASCADE, verbose_name="Konto wysyłkowe"
    )

    STATUS = (
        (MailingCampaignStatus.PAUSED, "Zatrzymano"),
        (MailingCampaignStatus.SENDING, "Wysyłanie"),
        (MailingCampaignStatus.DONE, "Zakończono"),
    )

    status = CharField(
        max_length=32, choices=STATUS, default=MailingCampaignStatus.PAUSED
    )

    # Allowed to send times
    allowed_to_send_after = TimeField(
        "Wysyłaj po", default=default_allowed_to_send_after
    )
    allowed_to_send_before = TimeField(
        "Wysyłaj do", default=default_allowed_to_send_before
    )

    # Subject
    subjects = TextField("Tytuły wiadomości e-mail")

    # Alias
    alias = CharField("Alias", max_length=64)

    # Template
    template = ForeignKey("MailingTemplate", on_delete=CASCADE)

    # Days
    monday = BooleanField(default=True)
    tuesday = BooleanField(default=True)
    wednesday = BooleanField(default=True)
    thursday = BooleanField(default=True)
    friday = BooleanField(default=True)
    saturday = BooleanField(default=False)
    sunday = BooleanField(default=False)

    # Metadata
    # emails_count_display = CharField(  # TODO
    #     "Ilość e-maili (cache)", max_length=32, default="0"
    # )

    class Meta:
        verbose_name = "Mailing Kampania"
        verbose_name_plural = "Mailing Kampanie"

    def __str__(self) -> str:
        return f"{self.title}"

    def get_subjects(self):
        """Get random subject"""
        # pylint: disable=no-member
        return [_.strip("\n\r") for _ in self.subjects.split("\n") if _]

    def get_random_subject(self):
        """Get random subject"""
        return choices(self.get_subjects())[0]