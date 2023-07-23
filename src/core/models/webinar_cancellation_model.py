import uuid

from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    ForeignKey,
    Model,
    UUIDField,
)


class WebinarApplicationCancellation(Model):
    """Represents webinar cancellation message for given application"""

    application = ForeignKey("WebinarApplication", on_delete=CASCADE)

    email_open_detected = BooleanField(
        "Wykryto otwarcie wiadomości e-mail", default=False
    )

    clicked_in_link = BooleanField("Kliknięto w link", default=False)

    token = UUIDField("Token odwołania szkolenia", default=uuid.uuid4)

    confirmed = BooleanField(
        "Przyjęto odwołanie",
        default=False,
        help_text="Przyjęto do wiadomości, że szkolenie jest odwołane",
    )

    discount_code = CharField("Kod rabatowy", max_length=32, blank=True)

    class Meta:
        verbose_name = "Odwołanie szkolenia"
        verbose_name_plural = "Odwołania szkoleń"

    def __str__(self) -> str:
        return f"Odwołanie #{self.id}"  # type: ignore
