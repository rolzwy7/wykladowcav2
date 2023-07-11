from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """User model"""

    username = models.EmailField(
        _("username"),
        unique=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    def __str__(self) -> str:
        return f"{self.username}"

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        self.email = self.username
        super().save(*args, **kwargs)
