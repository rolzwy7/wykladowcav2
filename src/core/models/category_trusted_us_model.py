"""
Model representing company that `trusted us`
"""

# flake8: noqa=E501
# pylint: disable=line-too-long

from django.db.models import (
    RESTRICT,
    BooleanField,
    CharField,
    ForeignKey,
    ImageField,
    Manager,
    Model,
    PositiveSmallIntegerField,
    QuerySet,
)


class CategoryTrustedUsManager(Manager):
    """Category Trusted Us Manager"""

    def get_visible(self) -> QuerySet["CategoryTrustedUs"]:
        """Get visible categories"""
        return self.get_queryset().filter(visible=True)


class CategoryTrustedUs(Model):
    """Represents webinar's category"""

    manager = CategoryTrustedUsManager()

    visible = BooleanField("Widoczna na stronie", default=True)
    category = ForeignKey("WebinarCategory", on_delete=RESTRICT)
    company_name = CharField("Nazwa firmy", max_length=100)

    company_logo = ImageField(
        "Logo firmy",
        upload_to="uploads/trusted_us_logos",
        help_text=(
            "Obrazek powinien być dobrej jakości o wymiarach najlepiej kwadratowych"
        ),
    )

    order = PositiveSmallIntegerField(
        "Pozycja",
        default=100,
        help_text=("Im niższa wartość tym wyższa pozycja kategorii przy wyświetlaniu"),
    )

    def __str__(self) -> str:
        return f"{self.company_name}"

    class Meta:
        verbose_name = "Kategoria (zaufali name)"
        verbose_name_plural = "Kategorie (zaufali name)"

    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)
