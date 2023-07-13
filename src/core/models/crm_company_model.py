from django.db.models import CharField, DateTimeField, Model

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

    name = CharField("Nazwa Firmy", max_length=500)

    class Meta:
        verbose_name = "CRM Firma"
        verbose_name_plural = "CRM Firmy"

    def __str__(self) -> str:
        return f"{self.nip}"
