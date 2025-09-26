"""Blog Model"""

# flake8: noqa=E501

import uuid

from django.db.models import (
    RESTRICT,
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    ImageField,
    Manager,
    ManyToManyField,
    Model,
    PositiveIntegerField,
    Q,
    QuerySet,
    SlugField,
    TextChoices,
    TextField,
    URLField,
    UUIDField,
)
from django.utils import timezone
from django.utils.text import slugify

# flake8: noqa=E501


class BlogPostQuerySet(QuerySet):
    """Dedykowany QuerySet dla modelu BlogPost."""

    def published(self):
        """Zwraca tylko opublikowane artykuły, których data publikacji już minęła."""
        return self.filter(
            Q(status=self.model.Status.PUBLISHED) & Q(published_at__lte=timezone.now())
        )

    def with_related_data(self):
        """
        Optymalizuje zapytanie poprzez pobranie powiązanych obiektów
        (wykładowcy i kategorie) w jednym zapytaniu do bazy danych.
        Używa select_related dla relacji ForeignKey i prefetch_related dla ManyToManyField.
        """
        return self.select_related("lecturer").prefetch_related("categories")


class BlogPostManager(Manager):
    """Manager dla modelu BlogPost."""

    def get_queryset(self):
        """Używa dedykowanego BlogPostQuerySet."""
        return BlogPostQuerySet(self.model, using=self._db)

    def get_blog_posts_for_category_slugs(
        self, slugs: list[str]
    ) -> QuerySet["BlogPost"]:
        """get_blog_posts_for_category_slugs"""
        return (
            self.all_published_with_related()
            .published()
            .filter(categories__slug__in=slugs)
            .order_by("published_at")
        )

    # Możesz dodać "skróty" do najczęściej używanych metod z QuerySet
    # aby można było je wywołać bezpośrednio z managera, np. BlogPost.objects.published()

    def published(self):
        """Zwraca opublikowane artykuły."""
        return self.get_queryset().published()

    def all_published_with_related(self):
        """Zwraca wszystkie opublikowane artykuły wraz z powiązanymi danymi."""
        return self.get_queryset().published().with_related_data()


class BlogPost(Model):
    """BlogPost"""

    class Status(TextChoices):
        """Status"""

        DRAFT = "draft", "Szkic"
        PUBLISHED = "published", "Opublikowany"
        ARCHIVED = "archived", "Zarchiwizowany"

    manager = BlogPostManager()

    show_related_webinars = BooleanField(
        "Pokaż szkolenia powiązane tematycznie", default=False
    )

    show_closed_webinar_advert = BooleanField(
        "Pokaż reklame szkoleń zamkniętych", default=True
    )

    # Status and dates
    status = CharField(
        "Status", max_length=20, choices=Status.choices, default=Status.DRAFT
    )
    created_at = DateTimeField("Data utworzenia", auto_now_add=True)
    updated_at = DateTimeField("Data aktualizacji", auto_now=True)
    published_at = DateTimeField("Data publikacji", blank=True, null=True)

    # Cover Image
    cover_image = ImageField(
        "Zdjęcie okładkowe",
        upload_to="uploads/blog_covers/%Y/%m/%d/",
        blank=True,
        null=True,
    )

    # Basic fields
    title = CharField("Tytuł", max_length=200)
    slug = SlugField("Slug URL", max_length=250, unique=True, blank=True)
    excerpt = TextField("Krótki opis", max_length=500, blank=True)
    content = TextField("Treść artykułu")

    # SEO fields
    meta_title = CharField("Meta tytuł (SEO)", max_length=60, blank=True)
    meta_description = CharField("Meta opis (SEO)", max_length=160, blank=True)
    meta_keywords = CharField("Słowa kluczowe (SEO)", max_length=255, blank=True)

    # Lecturer
    lecturer = ForeignKey(
        "Lecturer", on_delete=SET_NULL, null=True, blank=True, verbose_name="Wykładowca"
    )

    # Author
    author = CharField(max_length=100, help_text="Autor")
    author_url = URLField(blank=True, null=True, help_text="Autor URL")

    # Reading time estimation
    reading_time = CharField("Czas czytania (minuty)", max_length=20, default="5 minut")

    # View count
    view_count = PositiveIntegerField("Liczba wyświetleń", default=0)

    categories = ManyToManyField(
        "WebinarCategory",
        related_name="blog_posts",
        help_text="Kategorie",
    )

    advert_aggregate = ForeignKey(
        "WebinarAggregate",
        on_delete=SET_NULL,
        verbose_name="Advert Agregat",
        null=True,
        blank=True,
    )
    advert_category = ForeignKey(
        "WebinarCategory",
        on_delete=SET_NULL,
        verbose_name="Advert Kategoria",
        null=True,
        blank=True,
    )

    advert_fixed_html = TextField("Reklama fixed", blank=True)

    advert_sticky_html = TextField("Reklama sticky", blank=True)

    class Meta:
        """Meta"""

        verbose_name = "Blog: artykuł"
        verbose_name_plural = "Blog: artykuły"
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        """__str__"""
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def main_category(self):
        """main_category"""
        return self.categories.filter(parent=None).first()


class BlogView(Model):
    """Tracks clicks on blog article."""

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = DateTimeField("Data wyświetlenia", auto_now_add=True)

    blog_post = ForeignKey(
        "BlogPost",
        on_delete=RESTRICT,
        null=True,
        blank=True,
        verbose_name="Blog post",
    )

    spy_object = ForeignKey(
        "SpyObject",
        on_delete=RESTRICT,
        null=True,
        blank=True,
        verbose_name="Spy Object",
    )

    class Meta:
        """Meta"""

        verbose_name = "Blog: Wyświetlenie"
        verbose_name_plural = "Blog: Wyświetlenia"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Blog view {self.id}"
