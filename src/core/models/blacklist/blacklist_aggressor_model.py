# flake8: noqa=E501

from django.db.models import DateTimeField, EmailField, Manager, Model, TextField


class BlacklistAggressorManager(Manager):
    """BlacklistAggressorManager"""

    ...


# TODO: finish BlacklistAggressor
class BlacklistAggressor(Model):
    """Represents blacklisted aggressor e-amil"""

    manager = BlacklistAggressorManager()

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    email = EmailField("Adres E-mail", primary_key=True)

    message_content = TextField("Treść wiadomości", blank=True)
    trigger_content = TextField("Co spowodowało wykrycie?", blank=True)

    class Meta:
        verbose_name = "Zablokowany e-mail (agresor)"
        verbose_name_plural = "Zablokowane e-maile (agresor)"

    def __str__(self) -> str:
        return f"{self.email}"

    def save(self, *args, **kwargs):
        # Make lowercase
        self.email = self.email.lower()
        super().save(*args, **kwargs)
