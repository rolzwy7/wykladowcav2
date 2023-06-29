from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    TextField,
)


class CrmTodo(Model):
    """Represents To-Do item"""

    created_at = DateTimeField(auto_now_add=True)
    is_done = BooleanField("Wykonano zadanie", default=False)

    title = CharField("Tytuł", max_length=350)
    html = TextField("Opis", blank=True)

    webinar = ForeignKey(
        "Webinar",
        on_delete=CASCADE,
        verbose_name="Webinar",
        null=True,
        blank=True,
    )

    application = ForeignKey(
        "WebinarApplication",
        on_delete=CASCADE,
        verbose_name="Zgłoszenie",
        null=True,
        blank=True,
    )

    icon = CharField("Ikona", max_length=64, blank=True)
    color = CharField("Kolor", max_length=64, blank=True)
    url = CharField("URL", max_length=200, blank=True)

    class Meta:
        verbose_name = "Zadanie"
        verbose_name_plural = "Zadania"
