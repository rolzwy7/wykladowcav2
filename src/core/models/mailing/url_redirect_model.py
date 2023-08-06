from django.db.models import Index, Model, URLField

# TODO:


class UrlRedirect(Model):
    """Represents URL redirect"""

    indexes = [
        Index(fields=["url"]),
    ]

    url = URLField()

    class Meta:
        verbose_name = "Przekierowanie URL"
        verbose_name_plural = "Przekierowania URL"


# TODO: Add google tracking
