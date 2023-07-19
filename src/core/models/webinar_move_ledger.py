from django.db.models import (
    CASCADE,
    DateTimeField,
    ForeignKey,
    Manager,
    Model,
    PositiveSmallIntegerField,
)


class WebinarMoveLedgerManager(Manager):
    """WebinarMoveLedger query Manager"""

    ...


class WebinarMoveLedger(Model):
    """Represents webinar participant"""

    manager = WebinarMoveLedgerManager()

    created_at = DateTimeField(auto_now_add=True)

    # Webinar
    webinar = ForeignKey("Webinar", on_delete=CASCADE, verbose_name="Webinar")

    # Move from datetime
    from_datetime = DateTimeField("Początkowy termin")

    # Move to datetime
    to_datetime = DateTimeField("Docelowy termin")

    participants_count = PositiveSmallIntegerField(
        "Ilość uczestników",
        help_text="Ilość uczestników w momencie przenoszenia",
    )

    class Meta:
        verbose_name = "Przeniesiony termin"
        verbose_name_plural = "Przeniesione terminy"

    def __str__(self) -> str:
        return f"WebinarMoveLedger #{self.id}"  # type: ignore
