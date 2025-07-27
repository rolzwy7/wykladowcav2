"""Blog Model"""

from datetime import datetime

from django.db import models
from django.utils.text import slugify

# flake8: noqa=E501


class BlogPost(models.Model):
    """BlogPost"""

    STATUS_CHOICES = [
        ("draft", "Szkic"),
        ("published", "Opublikowany"),
        ("archived", "Zarchiwizowany"),
    ]

    # Status and dates
    status = models.CharField(
        "Status", max_length=20, choices=STATUS_CHOICES, default="draft"
    )
    created_at = models.DateTimeField("Data utworzenia", auto_now_add=True)
    updated_at = models.DateTimeField("Data aktualizacji", auto_now=True)
    published_at = models.DateTimeField("Data publikacji", blank=True, null=True)
    visible_after = models.DateTimeField(
        default=datetime.now, help_text="Widoczny po dacie"
    )

    # Basic fields
    title = models.CharField("Tytuł", max_length=200)
    slug = models.SlugField("Slug URL", max_length=250, unique=True)
    content = models.TextField("Treść artykułu")
    excerpt = models.TextField("Krótki opis", max_length=500, blank=True)

    # SEO fields
    meta_title = models.CharField("Meta tytuł (SEO)", max_length=60, blank=True)
    meta_description = models.CharField("Meta opis (SEO)", max_length=160, blank=True)
    meta_keywords = models.CharField("Słowa kluczowe (SEO)", max_length=255, blank=True)

    # Author
    author = models.CharField(max_length=100, help_text="Name of the author")
    author_url = models.URLField(
        blank=True, null=True, help_text="URL to author's profile or website"
    )

    # Reading time estimation
    reading_time = models.PositiveIntegerField("Czas czytania (minuty)", default=5)

    # View count
    view_count = models.PositiveIntegerField("Liczba wyświetleń", default=0)

    categories = models.ManyToManyField(
        "WebinarCategory",
        related_name="blog_posts",
        help_text="Categories for the blog post",
    )

    class Meta:
        verbose_name = "Artykuł blogowy"
        verbose_name_plural = "Artykuły blogowe"
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        """__str__"""
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
