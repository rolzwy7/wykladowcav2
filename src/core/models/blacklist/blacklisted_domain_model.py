from django.db.models import CharField, DateTimeField, Manager, Model


class BlacklistedDomainManager(Manager):
    """BlacklistedDomainManager"""

    ...


class BlacklistedDomain(Model):
    """Represents blacklisted domain"""

    manager = BlacklistedDomainManager()

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    domain = CharField("Domena", max_length=100, primary_key=True)
    # TODO: validation, valid domain

    class Meta:
        verbose_name = "Zablokowana domena"
        verbose_name_plural = "Zablokowane domeny"

    def __str__(self) -> str:
        return f"{self.domain}"

    def save(self, *args, **kwargs):
        # Make lowercase
        self.domain = self.domain.lower()
        self.domain = self.domain.strip("@")
        super().save(*args, **kwargs)
