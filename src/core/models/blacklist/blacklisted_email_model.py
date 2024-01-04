"""
Blacklist e-mail model
"""

from django.db.models import (
    CharField,
    DateTimeField,
    EmailField,
    Manager,
    Model,
    TextField,
)

from core.models.enums import BLACKLIST_REASON_CHOICES, BlacklistReason


class BlacklistedEmailManager(Manager):
    """BlacklistedEmailManager"""

    ...


class BlacklistedEmail(Model):
    """Represents blacklisted domain"""

    manager = BlacklistedEmailManager()

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    email = EmailField("Adres E-mail", primary_key=True)

    reason = CharField(
        "Powód blokowania",
        choices=BLACKLIST_REASON_CHOICES,
        max_length=32,
        default=BlacklistReason.MANUAL,
    )

    message_content = TextField("Treść wiadomości e-mail", blank=True)

    class Meta:
        verbose_name = "Zablokowany e-mail"
        verbose_name_plural = "Zablokowane e-maile"

    def __str__(self) -> str:
        return f"{self.email}"

    def save(self, *args, **kwargs):
        # Make lowercase
        self.email = self.email.lower()
        super().save(*args, **kwargs)
