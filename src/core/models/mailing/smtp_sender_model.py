"""
SMTP Sender Model
"""

# flake8: noqa=E501

from datetime import time

from django.db.models import (
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
    FloatField,
    Manager,
    Model,
    PositiveIntegerField,
    PositiveSmallIntegerField,
    QuerySet,
    TimeField,
)


def default_allowed_to_send_after():
    """Default `allowed to send after` time"""
    return time(5, 0, 0, 0)


def default_allowed_to_send_before():
    """Default `allowed to send before` time"""
    return time(13, 0, 0, 0)


class SmtpSenderManager(Manager):
    """SmtpSender query Manager"""

    def get_senders_for_processing(self) -> QuerySet["SmtpSender"]:
        """get_senders_for_processing"""
        return self.get_queryset().filter(exclude_from_processing=False)


class SmtpSender(Model):
    """Represents SMTP sender"""

    manager = SmtpSenderManager()

    sender_alias = CharField("Alias konta wysyłkowego", max_length=32, blank=True)

    username = EmailField("Nazwa użytkownika")
    password = CharField("Hasło", max_length=255)

    # Incoming
    incoming_server_hostname = CharField("Serwer przychodzący Host", max_length=255)

    INCOMING_PORTS = [
        ("110", "110"),
        ("143", "143"),
        ("993", "993"),
        ("995", "995"),
    ]
    incoming_server_port = CharField(
        "Serwer przychodzący Port",
        max_length=5,
        choices=INCOMING_PORTS,
    )

    # Outgoing
    outgoing_server_hostname = CharField("Serwer wychodzący Host", max_length=255)

    OUTGOING_PORTS = [
        ("25", "25"),
        ("465", "465"),
        ("587", "587"),
    ]
    outgoing_server_port = CharField(
        "Serwer wychodzący Port",
        max_length=5,
        choices=OUTGOING_PORTS,
    )

    domain = CharField("Domena", max_length=100)

    ssl = BooleanField("SSL", default=False)

    reply_to = EmailField("Reply-To")

    exclude_from_processing = BooleanField(
        "Exclude from mailing processing", default=False
    )

    mailing_server = CharField(
        "Mailing server",
        max_length=32,
        blank=True,
        help_text="Example: N1, N2, S1, S2 ...",
    )

    bucket_id = PositiveSmallIntegerField(default=0)

    show_on_crm_panel = BooleanField("Pokaż na stronie CRM", default=True)

    ip_address = CharField("IP Address", max_length=32, blank=True)

    monitor_rbl = BooleanField("Monitoruj listę RBL", default=True)

    base_url_override = CharField(
        "Nadpisz base url",
        max_length=128,
        blank=True,
        help_text="Jeśli base url inny niż https://wykladowca.pl",
    )

    TALOS_IP_REPUTATION_CHOICES = [
        ("POOR", "Poor"),
        ("NEUTRAL", "Neutral"),
        ("GOOD", "Good"),
        ("NO_DATA", "Brak danych"),
    ]
    talos_ip_reputation_checked_at = DateTimeField(
        "Talos IP Reputation Checked At", null=True, blank=True
    )
    talos_ip_reputation = CharField(
        "talosintelligence reputacja",
        max_length=16,
        choices=TALOS_IP_REPUTATION_CHOICES,
        default="NO_DATA",
    )

    return_path = CharField("Return-Path", max_length=100, blank=True)

    resignation_list = CharField("Lista rezygnacji", max_length=32, default="default")

    allowed_to_send_after = TimeField(
        "Wysyłaj po godzinie", default=default_allowed_to_send_after
    )
    allowed_to_send_before = TimeField(
        "Wysyłaj do godziny", default=default_allowed_to_send_before
    )
    sending_batch_size = PositiveIntegerField(default=100)
    sleep_between_batches = PositiveIntegerField(default=10)
    sleep_every_send = FloatField(default=0.1)

    class Meta:
        """meta"""

        verbose_name = "Konto wysyłkowe"
        verbose_name_plural = "Konta wysyłkowe"

    def __str__(self) -> str:
        return f"{self.username}"
