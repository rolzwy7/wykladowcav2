from django.db.models import DateTimeField, EmailField, Model


class BlacklistedEmail(Model):
    """Represents blacklisted domain"""

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

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
