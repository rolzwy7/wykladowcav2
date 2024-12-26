"""Mailing scheduled model"""

# flake8: noqa=E501

from django.db.models import (
    SET_NULL,
    CharField,
    DateField,
    DateTimeField,
    ForeignKey,
    Manager,
    Model,
    TextField,
)

from core.models.enums.mailing_enums import MailingScheduledStatus


class MailingScheduledManager(Manager):
    """Scheduled mailing campaign manager"""

    ...


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

    schedule_after = DateTimeField(
        "Zaplanuj po dacie", help_text="Po jakiej dacie ma być stworzona kampania"
    )

    target_date = DateField(
        "Mailing na dzień", help_text="Kiedy ma się wysyłać kampania"
    )

    url = CharField("URL szablonu", max_length=512)

    title = CharField("Tytuł kampanii", max_length=100)

    subjects = TextField("Tytuły wiadomości e-mail")

    alias = CharField("Alias", max_length=64)

    tags = TextField(
        "Tagi",
        blank=True,
        help_text="Z jakich tagów mają zostać wrzucone adresy e-mail",
    )

    class Meta:
        verbose_name = "Mailing Kampania (Zaplanowana)"
        verbose_name_plural = "Mailing Kampanie (Zaplanowane)"

    # def __str__(self):
    #     return f"{self.name}"

    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)
