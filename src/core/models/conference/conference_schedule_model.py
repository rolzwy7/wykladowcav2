# flake8: noqa=E501
# pylint: disable=line-too-long

from django.db.models import (
    CASCADE,
    RESTRICT,
    CharField,
    ForeignKey,
    Manager,
    Model,
    SlugField,
    TextField,
    TimeField,
)


class ConferenceScheduleManager(Manager):
    """ConferenceScheduleManager"""

    ...


class ConferenceSchedule(Model):
    """Represents CRM Company"""

    manager = ConferenceScheduleManager()

    title = CharField("Tytuł wpisu", max_length=230)

    edition = ForeignKey("ConferenceEdition", on_delete=CASCADE, verbose_name="Edycja")

    lecturer = ForeignKey(
        "Lecturer", on_delete=RESTRICT, verbose_name="Wykładowca", null=True, blank=True
    )

    short_description = TextField("Krótki opis", blank=True)

    hour_from = TimeField("Godzina od")

    hour_to = TimeField("Godzina do")

    html = TextField("Treść HTML", blank=True)

    class Meta:
        verbose_name = "Konferencja (harmonogram)"
        verbose_name_plural = "Konferencje (harmonogram)"

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)
