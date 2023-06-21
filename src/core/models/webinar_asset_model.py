from django.db.models import CASCADE, CharField, FileField, ForeignKey, Model


class WebinarAsset(Model):
    class Meta:
        verbose_name = "Materiał szkoleniowy"
        verbose_name_plural = "Materiałt szkoleniowe"

    webinar = ForeignKey("Webinar", on_delete=CASCADE, verbose_name="Webinar")

    title = CharField("Tytuł", max_length=300)

    attachment = FileField("Plik")
