import uuid

from django.db.models import BooleanField, EmailField, Model, UUIDField

# TODO:


class MailingUnsubscribe(Model):
    class Meta:
        verbose_name = "Rezygnacja"
        verbose_name_plural = "Rezygnacje"

    email = EmailField(primary_key=True)
    access_token = UUIDField(default=uuid.uuid4)
    unsubscribed = BooleanField(default=False)
