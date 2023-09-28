from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    ForeignKey,
    Manager,
    Model,
    PositiveSmallIntegerField,
    Q,
    QuerySet,
    SlugField,
    TextField,
)

from core.consts import SLUG_HELP_TEXT
from core.utils.text import slugify


class WebinarCategoryManager(Manager):
    """Webinar category manager"""

    def get_main_categories(self) -> QuerySet["WebinarCategory"]:
        """Get main categories (visible categories without parents)"""
        return (
            self.get_queryset()
            .filter(Q(visible=True) & Q(parent=None))
            .order_by("order")
        )

    def get_subcategories(
        self, category: "WebinarCategory"
    ) -> QuerySet["WebinarCategory"]:
        """Get subcategories for given category"""
        return (
            self.get_queryset()
            .filter(Q(visible=True) & Q(parent=category))
            .order_by("order")
        )


class WebinarCategory(Model):
    """Represents webinar's category"""

    manager = WebinarCategoryManager()

    visible = BooleanField("Widoczna na stronie", default=True)
    name = CharField("Nazwa kategorii", max_length=100)
    short_description = CharField("Krótki opis", max_length=100, blank=True)
    icon_html = TextField("Ikona HTML", blank=True)

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
    is_homepage_category = BooleanField("Jest kategorią domową", default=False)
    # is_new_category = BooleanField(
    #     "Jest kategorią domową",
    #     default=False,
    #     help_text="Kategoria jest nowa",
    # )

    about_html = TextField("Opis kategorii", default="[Opis kategorii]")

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

    def __str__(self):
        if self.parent:
            return f"{str(self.parent.name)}/{str(self.name)}"
        else:
            return str(self.name)

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
