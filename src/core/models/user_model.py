import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import EmailField, UUIDField
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """User model"""

    username = EmailField(
        _("username"),
        unique=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    activation_token = UUIDField("Token aktywacyjny", default=uuid.uuid4)

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.username}"

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        self.email = self.username
        super().save(*args, **kwargs)
