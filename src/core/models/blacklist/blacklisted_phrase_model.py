from django.db.models import CharField, DateTimeField, Model


class BlacklistedPhrase(Model):
    """Represents blacklisted phrase"""

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    phrase = CharField("Fraza", max_length=64, primary_key=True)

    class Meta:
        verbose_name = "Zablokowana fraza"
        verbose_name_plural = "Zablokowane frazy"

    def __str__(self) -> str:
        return f"{self.phrase}"

    def save(self, *args, **kwargs):
        # Make lowercase
        self.phrase = self.phrase.lower()
        super().save(*args, **kwargs)
