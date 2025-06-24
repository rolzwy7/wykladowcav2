"""
SMTP Sender Model
"""

# flake8: noqa=E501
import hashlib

from django.db.models import CharField, Model, PositiveIntegerField


class MailingTitleTest(Model):
    """MailingTitleTest"""

    # id

    campaign_id = CharField("ID kampanii mailingowej", max_length=32)

    title = CharField("Tytuł kampanii", max_length=200)

    sha256_hash = CharField("sha256", max_length=80, blank=True)

    counter = PositiveIntegerField("counter", default=0)

    def save(self, *args, **kwargs):
        value = f"{self.campaign_id}:{self.title}"
        self.sha256_hash = hashlib.sha256(value.encode("utf-8")).hexdigest()
        super().save(*args, **kwargs)

    class Meta:
        """meta"""

        verbose_name = "Mailing test tytuł"
        verbose_name_plural = "Mailing test tytuł"
