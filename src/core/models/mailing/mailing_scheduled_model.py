"""Mailing scheduled model"""

# flake8: noqa=E501

from django.db.models import (
    CASCADE,
    SET_NULL,
    CharField,
    DateField,
    DateTimeField,
    ForeignKey,
    Manager,
    Model,
    Q,
    QuerySet,
    TextField,
)
from django.utils.timezone import now

from core.models.enums.mailing_enums import MailingScheduledStatus


class MailingScheduledManager(Manager):
    """Scheduled mailing campaign manager"""

    def get_ready_to_schedule(self) -> QuerySet["MailingScheduled"]:
        """Returns ready to schedule mailings"""
        return self.get_queryset().filter(
            Q(status__in=[MailingScheduledStatus.INIT])
            & Q(schedule_after__lt=now())
            & Q(smtp_sender__isnull=False)
        )


class MailingScheduled(Model):
    """Represents scheduled mailing"""

    manager = MailingScheduledManager()

    created_at = DateTimeField(auto_now_add=True)

    STATUS = (
        (MailingScheduledStatus.INIT, "Do zaplanowania"),
        (MailingScheduledStatus.SCHEDULED, "Zaplanowano"),
        (MailingScheduledStatus.CANCELED, "Odwołano zaplanowanie"),
    )

    status = CharField(
        max_length=32, choices=STATUS, default=MailingScheduledStatus.INIT
    )

    smtp_sender = ForeignKey(
        "SmtpSender",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name="Konto wysyłkowe",
    )

    webinar = ForeignKey(
        "Webinar",
        verbose_name="Szkolenie",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        help_text="Jakiego szkolenia dotyczy mailing?",
    )

    campaign_id = ForeignKey(
        "MailingCampaign",
        verbose_name="Stworzona kampania",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        help_text="Jaka kampania została stworzona",
    )

    scheduled_at = DateTimeField(
        "Stworzony automatycznie",
        null=True,
        blank=True,
        help_text="Kiedy automat stworzył kampanie?",
    )

    schedule_after = DateTimeField(
        "Zaplanuj po dacie", help_text="Po jakiej dacie ma być stworzona kampania?"
    )

    target_date = DateField(
        "Mailing na dzień", help_text="Kiedy ma się wysyłać kampania?"
    )

    target_code = CharField("target_code", max_length=32, blank=True)

    url = CharField("URL szablonu", max_length=512)

    template = ForeignKey("MailingTemplate", blank=True, null=True, on_delete=CASCADE)

    title = CharField("Tytuł kampanii", max_length=100)

    subjects = TextField("Tytuły wiadomości e-mail")

    alias = CharField("Alias", max_length=64)

    resignation_list = CharField("Lista rezygnacji", max_length=32, default="default")

    tags = TextField(
        "Tagi",
        blank=True,
        help_text="Z jakich tagów mają zostać wrzucone adresy e-mail",
    )

    logi = TextField(
        "Logi",
        blank=True,
        help_text="Logi",
    )

    class Meta:
        """Meta"""

        verbose_name = "Mailing Kampania (Zaplanowana)"
        verbose_name_plural = "Mailing Kampanie (Zaplanowane)"

    # def __str__(self):
    #     return f"{self.name}"

    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)
