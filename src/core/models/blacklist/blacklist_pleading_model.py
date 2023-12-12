# flake8: noqa=E501

from django.db.models import DateTimeField, EmailField, Manager, Model, TextField


class BlacklistPleadingManager(Manager):
    """BlacklistPleadingManager"""

    ...


# TODO: finish BlacklistPleading
class BlacklistPleading(Model):
    """Represents blacklisted pleading e-amil"""

    manager = BlacklistPleadingManager()

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    email = EmailField("Adres E-mail", primary_key=True)

    message_content = TextField("Treść wiadomości", blank=True)
    trigger_content = TextField("Co spowodowało wykrycie?", blank=True)

    class Meta:
        verbose_name = "Zablokowany e-mail (prośba)"
        verbose_name_plural = "Zablokowane e-maile (prośba)"

    def __str__(self) -> str:
        return f"{self.email}"

    def save(self, *args, **kwargs):
        # Make lowercase
        self.email = self.email.lower()
        super().save(*args, **kwargs)
