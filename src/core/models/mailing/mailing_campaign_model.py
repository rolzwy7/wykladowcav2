from datetime import time
from random import choices

from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    F,
    ForeignKey,
    Manager,
    Model,
    PositiveIntegerField,
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
            & Q(send_after__lt=now())
            & Q(limit_sent_so_far__lte=F("limit_per_day"))
        )

    def not_done(self) -> QuerySet["MailingCampaign"]:
        """Returns mailing campaigns that are not done"""
        return self.get_queryset().filter(~Q(status=MailingCampaignStatus.DONE))


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
    send_after = DateTimeField("Wysyłaj po", default=now)

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

    # Limit per day
    limit_timestamp = DateTimeField("Limit reset datetime", default=now)
    limit_per_day = PositiveIntegerField(
        "Limit wysłanych na dzień (0 = brak limitu)", default=0
    )
    limit_sent_so_far = PositiveIntegerField("Wysłano do tej pory", default=0)

    # Sending stats
    stat_sent = PositiveIntegerField("Wysłano (stat)", default=0)
    stat_procesed = PositiveIntegerField("Przetworzono (stat)", default=0)

    class Meta:
        verbose_name = "Mailing Kampania"
        verbose_name_plural = "Mailing Kampanie"

    def __str__(self) -> str:
        return f"{self.title}"

    def get_subjects(self):
        """Get subjects list"""
        # pylint: disable=no-member
        return [_.strip("\n\r") for _ in self.subjects.split("\n") if _]

    def get_random_subject(self):
        """Get random subject"""
        return choices(self.get_subjects())[0]

    @property
    def is_allowed_to_send(self):
        """Is campaign allowed to send e-mails"""
        return all(
            [
                self.status == MailingCampaignStatus.SENDING,
                self.allowed_to_send_after < now().time(),
                self.allowed_to_send_before > now().time(),
                self.send_after < now(),
            ]
        )

    @property
    def is_send_after_correct(self):
        """Is `send_after` field lesser then current time"""
        return self.send_after < now()

    @property
    def is_allowed_to_send_correct(self):
        """Is `allowed_to_send` field within current time"""
        return all(
            [
                self.allowed_to_send_after < now().time(),
                self.allowed_to_send_before > now().time(),
            ]
        )

    @property
    def send_processed_percent(self):
        """What is a percentage of sent / processed emails"""
        if self.stat_procesed == 0:
            return "?%"
        return f"{self.stat_sent/self.stat_procesed:.2%}"
