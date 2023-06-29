from django.db.models import DateTimeField, EmailField, Model


class CrmContact(Model):  # TODO
    """Represents Company"""

    created_at = DateTimeField(auto_now_add=True)

    email = EmailField("Adres E-mail", unique=True)

    class Meta:
        verbose_name = "Firma"
        verbose_name_plural = "Firmy"
