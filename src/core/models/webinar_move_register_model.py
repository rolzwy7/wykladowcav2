import uuid

from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Manager,
    Model,
    PositiveSmallIntegerField,
    UUIDField,
)

from .enums import ApplicationMoveStatus


class WebinarMoveRegisterManager(Manager):
    """WebinarMoveRegister query Manager"""

    ...


class WebinarMoveRegister(Model):
    """Represents webinar participant"""

    manager = WebinarMoveRegisterManager()

    created_at = DateTimeField(auto_now_add=True)

    # Webinar
    webinar = ForeignKey("Webinar", on_delete=CASCADE, verbose_name="Webinar")

    # Move from datetime
    from_datetime = DateTimeField("Początkowy termin")

    # Move to datetime
    to_datetime = DateTimeField("Docelowy termin")

    applications_count = PositiveSmallIntegerField(
        "Ilość zgłoszeń",
        help_text="Ilość zgłoszeń w momencie przenoszenia",
    )

    @property
    def register_items(self):
        """Get this register's items"""
        return WebinarMoveRegisterItem.objects.filter(move_register=self)

    class Meta:
        verbose_name = "Przeniesiony termin"
        verbose_name_plural = "Przeniesione terminy"

    def __str__(self) -> str:
        return f"WebinarMoveRegister #{self.id}"  # type: ignore


class WebinarMoveRegisterItem(Model):
    """Represents webinar participant"""

    # Ledger
    move_register = ForeignKey(
        "WebinarMoveRegister",
        on_delete=CASCADE,
        verbose_name="Rejestr przeniesień szkolenia",
    )

    application = ForeignKey(
        "WebinarApplication", on_delete=CASCADE, verbose_name="Zgłoszenie"
    )

    token = UUIDField("Token odwołania szkolenia", default=uuid.uuid4)

    APPLICATION_MOVE_STATUS = [
        (ApplicationMoveStatus.INIT, "Wysłano zapytanie"),
        (ApplicationMoveStatus.ACCEPTED, "Akceptuje"),
        (ApplicationMoveStatus.ACCEPTED_WITH_DISCOUNT, "Akceptuje (zniżka)"),
        (ApplicationMoveStatus.RESIGNATION, "Rezygnacja"),
    ]

    status = CharField(
        max_length=32,
        default=ApplicationMoveStatus.INIT,
        choices=APPLICATION_MOVE_STATUS,
    )

    email_open_detected = BooleanField(
        "Wykryto otwarcie wiadomości e-mail", default=False
    )
    clicked_accept_link = BooleanField(
        "Kliknięto w przycisk 'Akceptuję'", default=False
    )
    clicked_resignation_link = BooleanField(
        "Kliknięto w przycisk 'Rezygnuję'", default=False
    )

    class Meta:
        verbose_name = "Przeniesione zgłoszenie"
        verbose_name_plural = "Przeniesione zgłoszenia"

    def __str__(self) -> str:
        return f"WebinarMoveRegisterItem #{self.id}"  # type: ignore
