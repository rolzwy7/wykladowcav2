"""
Lead model
"""
# flake8: noqa:E501
# pylint: disable=line-too-long

from django.db.models import (
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
    Manager,
    Model,
    TextField,
)

# TODO: finish LeadMailboxReplyModel


class LeadMailboxReplyManager(Manager):
    """Lead mailbox reply query Manager"""

    ...


class LeadMailboxReplyModel(Model):
    """This model represents Lecturer"""

    manager = LeadMailboxReplyManager()

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    processed = BooleanField("Przetworzono?", default=False)

    from_email = EmailField("Adres E-mail", unique=True)
    subject = CharField("Tytuł wiadomości", max_length=400)

    message_content = TextField("Treść wiadomości", blank=True)
    trigger_content = TextField("Co spowodowało wykrycie?", blank=True)

    class Meta:
        verbose_name = "Lead (Odp. e-mail)"
        verbose_name_plural = "Lead'y (Odp. e-mail)"

    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)
