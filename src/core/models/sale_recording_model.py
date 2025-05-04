"""Recording For Sale Model"""

# flake8: noqa


from django.db.models import (
    RESTRICT,
    BooleanField,
    DateTimeField,
    ForeignKey,
    Manager,
    Model,
    Q,
    QuerySet,
)


class SaleRecordingManager(Manager):
    """SaleRecordingManager query Manager"""

    def get_ready_for_sale(self) -> QuerySet["SaleRecording"]:
        """get_ready_for_sale"""
        return self.get_queryset().filter(is_visible=True)


class SaleRecording(Model):
    """Represents recording for sale"""

    manager = SaleRecordingManager()

    created_at = DateTimeField(auto_now_add=True)

    is_visible = BooleanField(
        "Widoczne na stronie",
        default=True,
        help_text="Pokaż nagranie na sprzedaż na stronie",
    )

    recording = ForeignKey(
        "WebinarRecording", verbose_name="Nagranie", on_delete=RESTRICT
    )

    def __str__(self) -> str:
        return f"Nagranie na sprzedaż ID={self.recording}"

    class Meta:
        verbose_name = "Nagranie na sprzedaż"
        verbose_name_plural = "Nagrania na sprzedaż"
        ordering = ["-created_at"]
