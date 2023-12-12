from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Manager,
    Model,
    TextField,
)


class CrmTodoManager(Manager):
    """CrmTodoManager"""

    ...


class CrmTodo(Model):
    """Represents To-Do item"""

    manager = CrmTodoManager()

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

    def __str__(self) -> str:
        return f"{self.title}"
