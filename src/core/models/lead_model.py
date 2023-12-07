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
)


class LeadManager(Manager):
    """Lead query Manager"""

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    email = EmailField("Adres E-mail", unique=True)

    first_name = CharField("Imię", max_length=100, blank=True)
    last_name = CharField("Nazwisko", max_length=100, blank=True)

    ip_address = CharField(max_length=64, blank=True)

    is_aggressor = BooleanField("Czy jest agresorem?", default=False)
    is_customer = BooleanField("Czy był klientem?", default=False)
    detected_bot_click = BooleanField("Wykryto kliknięcie bota?", default=False)

    last_email_date = DateTimeField(null=True)
    last_email_opened = DateTimeField(null=True)
    last_email_clicked = DateTimeField(null=True)
    last_purchase_date = DateTimeField(null=True)
    last_activity_date = DateTimeField(null=True)


class LeadModel(Model):
    """This model represents Lecturer"""

    manager = LeadManager()

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Lead'y"

    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)
