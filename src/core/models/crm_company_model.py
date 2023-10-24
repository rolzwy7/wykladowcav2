from django.db.models import (
    BooleanField,
    CharField,
    DateTimeField,
    Model,
    TextField,
)

from core.libs.validators import validate_nip_modelfield


class CrmCompany(Model):
    """Represents CRM Company"""

    created_at = DateTimeField(auto_now_add=True)

    nip = CharField(
        "NIP",
        max_length=32,
        unique=True,
        validators=[validate_nip_modelfield],
    )

    is_nonpaying = BooleanField(
        "Niepłacący",
        default=False,
        help_text="Ten klient nie zapłacił za fakturę w przeszłości",
    )

    notes = TextField("Notatki", blank=True)

    name = CharField("Nazwa Firmy", max_length=500)

    class Meta:
        verbose_name = "CRM Firma"
        verbose_name_plural = "CRM Firmy"

    def __str__(self) -> str:
        return f"{self.nip}"

    def save(self, *args, **kwargs) -> None:
        self.nip = self.nip.replace(" ", "").replace("-", "")
        return super().save(*args, **kwargs)
