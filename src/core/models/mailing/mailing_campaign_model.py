"""Mailing campaign model"""

# flake8: noqa=E501
# pylint: disable=unnecessary-negation
# pylint: disable=superfluous-parens

from datetime import time
from random import choices

from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Manager,
    Model,
    PositiveIntegerField,
    PositiveSmallIntegerField,
    Q,
    QuerySet,
    TextField,
    TimeField,
)
from django.template.defaultfilters import date as _date
from django.utils.timezone import now, timedelta

from core.models.enums import MailingCampaignStatus


def default_allowed_to_send_after():
    """Default `allowed to send after` time"""
    return time(5, 0, 0, 0)


def default_allowed_to_send_before():
    """Default `allowed to send before` time"""
    return time(13, 0, 0, 0)


class MailingCampaignManager(Manager):
    """Mailing campaign manager"""

    def active_campaigns(self) -> QuerySet["MailingCampaign"]:
        """Returns active mailing campaigns"""
        return self.get_queryset().filter(
            Q(status=MailingCampaignStatus.SENDING)
            & Q(allowed_to_send_after__lt=now())
            & Q(allowed_to_send_before__gt=now())
            & Q(send_after__lt=now())
        )

    def active_campaigns_random_order(self) -> QuerySet["MailingCampaign"]:
        """Returns active mailing campaigns"""
        return (
            self.get_queryset()
            .filter(
                Q(status=MailingCampaignStatus.SENDING)
                & Q(allowed_to_send_after__lt=now())
                & Q(allowed_to_send_before__gt=now())
                & Q(send_after__lt=now())
            )
            .order_by("?")
        )

    def active_campaigns_for_processing(self) -> QuerySet["MailingCampaign"]:
        """Returns active mailing campaigns for processing process"""
        return self.get_queryset().filter(
            Q(status=MailingCampaignStatus.SENDING)
            & Q(allowed_to_send_after__lt=now() + timedelta(hours=6))
            & Q(allowed_to_send_before__gt=now())
            & Q(send_after__lt=now() + timedelta(hours=6))
        )

    def sending_status_campaigns(self) -> QuerySet["MailingCampaign"]:
        """Returns mailing campaigns with SENDING status"""
        return self.get_queryset().filter(status=MailingCampaignStatus.SENDING)

    def paused_status_campaigns(self) -> QuerySet["MailingCampaign"]:
        """Returns mailing campaigns with PAUSED status"""
        return self.get_queryset().filter(status=MailingCampaignStatus.PAUSED)

    def not_done(self) -> QuerySet["MailingCampaign"]:
        """Returns mailing campaigns that are not done"""
        return self.get_queryset().filter(~Q(status=MailingCampaignStatus.DONE))

    def favourite(self) -> QuerySet["MailingCampaign"]:
        """Returns favourite mailing campaigns"""
        return self.get_queryset().filter(favourite=True)


class MailingCampaign(Model):
    """Represents mailing campaign"""

    manager = MailingCampaignManager()

    webinar = ForeignKey(
        "Webinar",
        verbose_name="Szkolenie",
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )

    created_at = DateTimeField(auto_now_add=True)

    favourite = BooleanField("Ulubiona kampania", default=False)

    sent_start_at = DateTimeField(null=True, blank=True)

    target_code = CharField("target_code", max_length=32, blank=True)

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

    resignation_list = CharField("Lista rezygnacji", max_length=32, default="default")

    status = CharField(
        max_length=32, choices=STATUS, default=MailingCampaignStatus.PAUSED
    )

    # Allowed to send times
    allowed_to_send_after = TimeField(
        "Wysyłaj po godzinie", default=default_allowed_to_send_after
    )
    allowed_to_send_before = TimeField(
        "Wysyłaj do godziny", default=default_allowed_to_send_before
    )
    send_after = DateTimeField("Wysyłaj od dnia i godziny", default=now)

    # Subject
    subjects = TextField("Tytuły wiadomości e-mail")

    # Alias
    alias = CharField("Alias", max_length=64)

    # Template
    template = ForeignKey("MailingTemplate", on_delete=CASCADE)

    # Comment
    comment = TextField("Komentarz", blank=True)

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

    # Counters
    resets_counter = PositiveIntegerField("Ilość resetów", default=0)
    failure_counter = PositiveIntegerField(default=0)

    # Errors
    any_error_occured = BooleanField(default=False)
    smtp_server_disconnected = BooleanField(default=False)
    connection_refused = BooleanField(default=False)
    smtp_recipients_refused = BooleanField(default=False)

    # Priority
    base_priority = PositiveSmallIntegerField(default=100)
    random_priority = BooleanField(default=True)
    random_priority_min = PositiveSmallIntegerField(default=0)
    random_priority_max = PositiveSmallIntegerField(default=100)

    # Modulo value
    mod_value = PositiveSmallIntegerField(default=10)

    # Flags
    pause_on_too_many_failures = BooleanField(default=True)
    inherit_bucket_id_from_sender = BooleanField(default=True)

    # Clicks
    total_clicks = PositiveIntegerField(default=0)

    # Batch size and wait between batch sends
    sending_batch_size = PositiveIntegerField(default=100)
    sleep_between_batches = PositiveIntegerField(default=10)

    class Meta:
        """meta"""

        verbose_name = "Mailing Kampania"
        verbose_name_plural = "Mailing Kampanie"

    def __str__(self) -> str:
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.sent_start_at:
            self.sent_start_at = now() + timedelta(days=1)
        super().save(*args, **kwargs)

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
                self.send_after < now(),
                self.allowed_to_send_after < now().time(),
                self.allowed_to_send_before > now().time(),
            ]
        )

    @property
    def why_not_sending(self):
        """Explain why campaign is not sending"""

        if not (self.status == MailingCampaignStatus.SENDING):
            return "status != 'Wysyłanie'"

        if not (self.send_after < now()):
            return f"Rozpocznie po {_date(self.send_after, 'j E Y - H:i')}"

        if not (self.allowed_to_send_after < now().time()):
            return f"Obecny czas <  {self.allowed_to_send_after}"

        if not (self.allowed_to_send_before > now().time()):
            return f"Obecny czas > {self.allowed_to_send_before}"

        return ""

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
    def is_daily_sending_limit_reached(self):
        """Is daily sending limit reached"""
        return all(
            [self.limit_per_day != 0, self.limit_sent_so_far >= self.limit_per_day]
        )

    @property
    def status_color(self):
        """Get status color"""
        return {
            MailingCampaignStatus.PAUSED: "warning",
            MailingCampaignStatus.SENDING: "success",
            MailingCampaignStatus.DONE: "danger",
        }[self.status]

    @property
    def created_at_plus_one_day(self):
        """created_at_plus_one_day"""
        return self.created_at + timedelta(days=1)

    # def is_day_before
