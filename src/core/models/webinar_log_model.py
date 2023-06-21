from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    TextField,
)


class WebinarLog(Model):
    created_at = DateTimeField(auto_now_add=True)
    webinar = ForeignKey("Webinar", on_delete=CASCADE, verbose_name="Webinar")
    title = CharField(max_length=100)
    description = TextField(blank=True)

    # attachment
