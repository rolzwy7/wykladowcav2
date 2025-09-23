"""
E-mail message
"""

# flake8: noqa=E501

from django.db.models import (
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
    Manager,
    Model,
    TextField,
)


class MailingReplyMessageManager(Manager):
    """MailingReplyMessageManager"""

    ...


class MailingReplyMessage(Model):
    """Represents e-mail message sent to mailing address"""

    manager = MailingReplyMessageManager()

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    checked = BooleanField(default=False)

    email_id = CharField("Message ID", max_length=128, primary_key=True)

    from_email = EmailField("Adres E-mail (From)")
    to_email = EmailField("Adres E-mail (To)")

    is_aggressor = BooleanField(default=False)
    is_vacation = BooleanField(default=False)
    is_email_change = BooleanField(default=False)

    subject = CharField("Tytuł wiadomości", max_length=512)
    message_content = TextField("Treść wiadomości", blank=True)
    trigger_content = TextField("Co spowodowało wykrycie?", blank=True)

    class Meta:
        verbose_name = "Wiadomość e-mail"
        verbose_name_plural = "Wiadomości e-mail"

    def __str__(self) -> str:
        return f"{self.from_email}"

    def save(self, *args, **kwargs):
        # Make lowercase
        self.from_email = self.from_email.lower()
        super().save(*args, **kwargs)
