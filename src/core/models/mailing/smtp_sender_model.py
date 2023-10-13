from django.db.models import BooleanField, CharField, EmailField, Model


class SmtpSender(Model):
    """Represents SMTP sender"""

    username = EmailField("Nazwa użytkownika")
    password = CharField("Hasło", max_length=255)

    # Incoming
    incoming_server_hostname = CharField(
        "Serwer przychodzący Host", max_length=255
    )

    INCOMING_PORTS = [("995", "995")]
    incoming_server_port = CharField(
        "Serwer przychodzący Port",
        max_length=5,
        choices=INCOMING_PORTS,
    )

    # Outgoing
    outgoing_server_hostname = CharField(
        "Serwer wychodzący Host", max_length=255
    )

    OUTGOING_PORTS = [("465", "465")]
    outgoing_server_port = CharField(
        "Serwer wychodzący Port",
        max_length=5,
        choices=OUTGOING_PORTS,
    )

    domain = CharField("Domena", max_length=100)

    ssl = BooleanField("SSL", default=False)

    reply_to = EmailField("Reply-To")

    class Meta:
        verbose_name = "Konto wysyłkowe"
        verbose_name_plural = "Konta wysyłkowe"

    def __str__(self) -> str:
        return f"{self.username}"
