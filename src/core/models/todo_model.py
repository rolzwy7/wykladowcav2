from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    FileField,
    ForeignKey,
    Model,
    TextField,
    URLField,
)


class Todo(Model):
    created_at = DateTimeField(auto_now_add=True)

    title = CharField("Tytuł", max_length=350)
    description = TextField("Opis", blank=True)
    webinar = ForeignKey(
        "Webinar",
        on_delete=CASCADE,
        verbose_name="Webinar",
        null=True,
        blank=True,
    )
    url = URLField("URL", blank=True)
    attachment = FileField("Plik", blank=True)

    icon = CharField("Ikona", max_length=64, blank=True)
    color = CharField("Kolor", max_length=64, blank=True)
