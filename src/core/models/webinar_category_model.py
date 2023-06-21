from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    ForeignKey,
    Manager,
    Model,
    PositiveSmallIntegerField,
    QuerySet,
    SlugField,
)

from core.consts import SLUG_HELP_TEXT
from core.utils.text import slugify


class WebinarCategoryManager(Manager):
    def get_queryset(self):
        return super().get_queryset()

    def sidebar_categories(self) -> QuerySet["WebinarCategory"]:
        return self.get_queryset().filter()


class WebinarCategory(Model):
    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

    def __str__(self):
        return self.name

    manager = WebinarCategoryManager()

    visible = BooleanField("Widoczna na stronie", default=True)
    name = CharField("Nazwa kategorii", max_length=100)
    slug = SlugField(
        "Skrót URL",
        max_length=120,
        blank=True,
        unique=True,
        help_text=SLUG_HELP_TEXT,
    )
    parent = ForeignKey(
        "self",
        on_delete=CASCADE,
        blank=True,
        null=True,
        verbose_name="Rodzic",
        help_text=("Kategoria nadrzędna"),
    )
    order = PositiveSmallIntegerField(
        "Pozycja",
        default=100,
        help_text=(
            "Im niższa wartość tym wyższa pozycja kategorii przy wyświetlaniu"
        ),
    )

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
