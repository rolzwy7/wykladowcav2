from datetime import datetime

from django.db import models
from django.utils.text import slugify


class BlogPost(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
        ("archived", "Archived"),
    )

    slug = models.SlugField(
        max_length=250, unique=True, help_text="URL-friendly identifier"
    )
    add_date = models.DateTimeField(
        null=True, blank=True, help_text="Date the post was created"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
        help_text="Publication status",
    )
    visible_after = models.DateTimeField(
        default=datetime.now, help_text="Date after which the post is visible"
    )

    title_meta = models.CharField(
        max_length=200, help_text="SEO meta title for the blog post"
    )
    title_h1 = models.CharField(
        max_length=200, help_text="Main heading for the blog post"
    )

    author = models.CharField(max_length=100, help_text="Name of the author")
    author_url = models.URLField(
        blank=True, null=True, help_text="URL to author's profile or website"
    )

    image = models.ImageField(
        upload_to="blog_images/",
        blank=True,
        null=True,
        help_text="Featured image for the blog post",
    )

    html = models.TextField(help_text="HTML content of the blog post")

    categories = models.ManyToManyField(
        "WebinarCategory",
        related_name="blog_posts",
        help_text="Categories for the blog post",
    )

    class Meta:
        ordering = ["-visible_after"]
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return self.title_h1

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_h1)
        super().save(*args, **kwargs)
