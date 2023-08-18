from django.db.models import Index, Model, URLField


class UrlRedirect(Model):
    """Represents URL redirect"""

    url = URLField(primary_key=True)

    target_url = URLField()

    class Meta:
        verbose_name = "Przekierowanie URL"
        verbose_name_plural = "Przekierowania URL"


# TODO: Add google tracking
