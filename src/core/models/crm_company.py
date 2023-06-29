from django.db.models import CharField, DateTimeField, Model


class CrmCompany(Model):  # TODO
    """Represents Company"""

    created_at = DateTimeField(auto_now_add=True)

    name = CharField("Nazwa Firmy", max_length=500)

    class Meta:
        verbose_name = "Firma"
        verbose_name_plural = "Firmy"
