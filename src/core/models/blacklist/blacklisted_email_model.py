from django.db.models import EmailField, Model


class BlacklistedEmail(Model):
    """Represents blacklisted domain"""

    email = EmailField("Adres E-mail", primary_key=True)

    class Meta:
        verbose_name = "Zablokowany e-mail"
        verbose_name_plural = "Zablokowane e-maile"

    def __str__(self) -> str:
        return f"{self.email}"

    def save(self, *args, **kwargs):
        # Make lowercase
        self.email = self.email.lower()
        super().save(*args, **kwargs)
