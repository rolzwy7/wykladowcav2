"""
Webinar category model
"""

# flake8: noqa=E501
# pylint: disable=line-too-long

from django.db.models import (
    RESTRICT,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Manager,
    Model,
    PositiveSmallIntegerField,
    QuerySet,
    SlugField,
    TextField,
)

from core.consts import SLUG_HELP_TEXT
from core.utils.text import slugify


class WebinarCategoryManager(Manager):
    """Webinar category manager"""

    def get_visible_categories(self) -> QuerySet["WebinarCategory"]:
        """Get visible categories"""
        return self.get_queryset().filter(visible=True)

    def get_main_categories(self) -> QuerySet["WebinarCategory"]:
        """Get main categories (visible categories without parents)"""
        return self.get_visible_categories().filter(parent=None).order_by("order")

    def get_main_categories_alphabetical_order(self) -> QuerySet["WebinarCategory"]:
        """Get main categories (visible categories without parents, alphabetical_order)"""
        return self.get_visible_categories().filter(parent=None).order_by("name")

    def get_blog_categories(self) -> QuerySet["WebinarCategory"]:
        """Get blog categories"""
        return self.get_visible_categories().filter(blog_visible=True)

    def get_subcategories(
        self, category: "WebinarCategory"
    ) -> QuerySet["WebinarCategory"]:
        """Get all categories that have this category as a parent or grandparent"""
        return self.get_visible_categories().filter(parent=category)


class WebinarCategory(Model):
    """Represents webinar's category"""

    manager = WebinarCategoryManager()

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    blog_visible = BooleanField("Widoczna w blogu", default=False)

    visible = BooleanField("Widoczna na stronie", default=True)
    name = CharField("Nazwa kategorii", max_length=100)
    name_homepage = CharField(
        "Nazwa kategorii (strona główna)", max_length=100, blank=True
    )
    title = CharField("Tytuł kategorii", max_length=100, blank=True)
    short_description = CharField("Krótki opis", max_length=500, blank=True)
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
        on_delete=RESTRICT,
        blank=True,
        null=True,
        verbose_name="Rodzic",
        help_text=("Kategoria nadrzędna"),
    )
    order = PositiveSmallIntegerField(
        "Pozycja",
        default=100,
        help_text=("Im niższa wartość tym wyższa pozycja kategorii przy wyświetlaniu"),
    )

    about_html = TextField("Opis kategorii", default="[Opis kategorii]")

    fakturownia_category_id = CharField(
        "ID Kategorii w Fakturowni", max_length=32, blank=True
    )

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

    def __str__(self):
        if self.parent:
            return f"{str(self.parent.name)} > {str(self.name)}"
        else:
            return str(self.name)

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            if self.parent:
                self.slug = f"{slugify(self.name)}-{slugify(self.parent.name)}"
            else:
                self.slug = slugify(self.name)

        return super().save(*args, **kwargs)
