from django.db.models import CharField, DateTimeField, Manager, Model, TextField

# TODO: idea (TO DELETE ?)


class WebinarTopicManager(Manager):
    """Webinar Topic query Manager"""


class WebinarTopic(Model):
    """Represents webinar topic"""

    manager = WebinarTopicManager()

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    topic_shortname = CharField(
        "Krótka nazwa tematu",
        max_length=64,
        help_text="Aby było łatwiej rozpoznać w liście rozwijanej",
    )

    # Program
    program = TextField("Program szkolenia", default="[Program Szkolenia]")
    program_markdown = TextField("Program szkolenia (markdown)", blank=True)
    program_enchanted = TextField("Program szkolenia (enchanted)", blank=True)

    class Meta:
        verbose_name = "Temat webinaru"
        verbose_name_plural = "Tematy webinarów"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return str(self.topic_shortname)

    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)
