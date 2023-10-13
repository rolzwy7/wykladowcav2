from django.db.models import DateTimeField, EmailField, Model


class CrmContact(Model):
    """Represents CRM Contact"""

    created_at = DateTimeField(auto_now_add=True)

    email = EmailField("Adres E-mail", unique=True)

    class Meta:
        verbose_name = "CRM Reprezentant"
        verbose_name_plural = "CRM Reprezentanci"

    def __str__(self) -> str:
        return f"{self.email}"
