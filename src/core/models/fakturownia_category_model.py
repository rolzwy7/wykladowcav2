"""fakturownia_category_model"""

# flake8: noqa=E501

from django.db.models import CharField, Manager, Model


class FakturowniaCategoryManager(Manager):
    """FakturowniaCategoryManager"""

    ...


class FakturowniaCategory(Model):
    """RepresFakturowniaCategory"""

    manager = FakturowniaCategoryManager()

    fakturownia_id = CharField("ID w Fakturowni", max_length=32, primary_key=True)

    name = CharField("Nazwa", max_length=100)

    class Meta:
        verbose_name = "Fakturownia - Kategoria"
        verbose_name_plural = "Fakturownia - Kategorie"

    def __str__(self) -> str:
        return f"{self.name}"
