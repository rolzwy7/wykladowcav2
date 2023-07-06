from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    FileField,
    ForeignKey,
    Manager,
    Model,
    QuerySet,
)

from .webinar_model import Webinar


class WebinarAssetManager(Manager):
    """Webinar asset query Manager"""

    def get_for_webinar(self, webinar: Webinar) -> QuerySet["Webinar"]:
        """Get assets for webinar"""
        return self.get_queryset().filter(webinar=webinar)


class WebinarAsset(Model):
    """Represents webinar's asset"""

    manager = WebinarAssetManager()

    created_at = DateTimeField(auto_now_add=True)

    webinar = ForeignKey("Webinar", verbose_name="Webinar", on_delete=CASCADE)

    filename = CharField("Nazwa pliku", max_length=300)

    filesize = CharField("Rozmiar pliku", max_length=80)

    content_type = CharField("Typ MIME", max_length=100)

    file = FileField("Plik", upload_to="uploads/webinar_assets")

    @property
    def filesize_human(self):
        suffix = "B"
        num = int(self.filesize)
        for unit in ("", "K", "M", "G", "T", "P", "E", "Z"):
            if abs(num) < 1024.0:
                return f"{num:3.1f} {unit}{suffix}"
            num /= 1024.0
        return f"{num:.1f} Y{suffix}"

    class Meta:
        verbose_name = "Materiał szkoleniowy"
        verbose_name_plural = "Materiały szkoleniowe"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.filename}"
