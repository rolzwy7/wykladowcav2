from django.db.models import (
    CharField,
    DateTimeField,
    Manager,
    Model,
    PositiveIntegerField,
)


class RedirectManualManager(Manager):
    """Contact Message Manager"""

    ...


class RedirectManual(Model):
    """Represents webinar's asset"""

    manager = RedirectManualManager()

    created_at = DateTimeField(auto_now_add=True)

    slug = CharField("Slug", max_length=350, primary_key=True)

    url = CharField("URL", max_length=350)

    STATUS_CODES = [
        ("301", "(301) Moved Permanently"),
        ("302", "(302) Found"),
        ("307", "(307) Temporary Redirect"),
        ("308", "(308) Permanent Redirect"),
    ]

    status_code = CharField("Status code", max_length=10, choices=STATUS_CODES)

    counter = PositiveIntegerField("Redirect counter", default=0)

    class Meta:
        verbose_name = "Przekierowanie (manualne)"
        verbose_name_plural = "Przekierowania (manualne)"

    def __str__(self) -> str:
        return f"({self.slug})"
