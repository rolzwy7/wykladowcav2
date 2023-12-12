from django.db.models import DateTimeField, EmailField, Manager, Model
from django.utils.timezone import now, timedelta


def default_expires_at():
    """Default expiration timedelta for temporary blacklist"""
    return now() + timedelta(days=14)


class BlacklistedEmailTemporaryManager(Manager):
    """BlacklistedEmailTemporaryManager"""

    ...


class BlacklistedEmailTemporary(Model):
    """Represents temporarily blacklisted email"""

    manager = BlacklistedEmailTemporaryManager()

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    email = EmailField("Adres E-mail", primary_key=True)

    expires_at = DateTimeField(
        "Wygasa",
        default=default_expires_at,
        help_text="Kiedy zablokowanie wygasa",
    )

    @property
    def is_expired(self):
        """Is temporary blocking expired"""
        return now() > self.expires_at

    class Meta:
        verbose_name = "Zablokowane tymczasowo emaile"
        verbose_name_plural = "Zablokowane tymczasowo email"

    def __str__(self) -> str:
        return f"{self.email}"

    def save(self, *args, **kwargs):
        # Make lowercase
        self.email = self.email.lower()
        super().save(*args, **kwargs)
