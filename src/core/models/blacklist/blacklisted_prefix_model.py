from django.db.models import CharField, DateTimeField, Model


class BlacklistedPrefix(Model):
    """Represents blacklisted prefix"""

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    prefix = CharField("Prefiks", max_length=100, primary_key=True)

    class Meta:
        verbose_name = "Zablokowany prefix"
        verbose_name_plural = "Zablokowane prefixy"

    def __str__(self) -> str:
        return f"{self.prefix}"

    def save(self, *args, **kwargs):
        # Make lowercase
        self.prefix = self.prefix.lower()
        self.prefix = self.prefix.strip("@")
        super().save(*args, **kwargs)
