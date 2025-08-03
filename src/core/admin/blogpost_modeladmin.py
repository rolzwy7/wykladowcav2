"""
BlogPost Model Admin
"""

# flake8: noqa=E501

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """
    Konfiguracja panelu administracyjnego dla modelu BlogPost.
    """

    # --- Konfiguracja widoku listy ---

    # Pola wyświetlane w tabeli z listą artykułów
    list_display = (
        "title",
        "status",
        "lecturer",
        "published_at",
        "view_count",
    )

    # Filtry, które pojawią się w panelu bocznym
    list_filter = (
        "status",
        "lecturer",
        "categories",
        "published_at",
    )

    # Pola, po których będzie można przeszukiwać artykuły
    # Uwaga: Zakładamy, że model Lecturer ma pola first_name i last_name
    search_fields = (
        "title",
        "content",
        "lecturer__first_name",
        "lecturer__last_name",
    )

    # Dodaje nawigację po datach na górze listy
    date_hierarchy = "published_at"

    # Domyślne sortowanie listy
    ordering = ("-published_at", "-created_at")

    # --- Konfiguracja formularza edycji/dodawania ---

    # Automatycznie wypełnia pole 'slug' na podstawie wartości z 'title'
    prepopulated_fields = {"slug": ("title",)}

    # Używa prostszego widgetu dla klucza obcego, gdy jest wiele opcji (np. wykładowców)
    # Zamiast listy <select>, pojawi się pole do wpisania ID z lupką do wyszukiwania.
    raw_id_fields = ("lecturer",)

    # Zmienia domyślny widget dla pól ManyToManyField na bardziej przyjazny
    filter_horizontal = ("categories",)

    # Pola, które będą tylko do odczytu w panelu admina
    readonly_fields = ("created_at", "updated_at", "view_count")

    # Grupuje pola w sekcje (fieldsets) dla lepszej organizacji formularza
    fieldsets = (
        (
            None,
            {"fields": ("show_related_webinars",)},
        ),
        (
            _("Treść i okładka"),
            {"fields": ("title", "slug", "cover_image", "excerpt", "content")},
        ),
        (
            _("Status i publikacja"),
            {"fields": ("status", "published_at", "created_at", "updated_at")},
        ),
        (
            _("Dane SEO"),
            {
                "fields": ("meta_title", "meta_description", "meta_keywords"),
            },
        ),
        (
            _("Autor i powiązania"),
            {
                "fields": (
                    "author",
                    "author_url",
                    "lecturer",
                    "categories",
                ),
            },
        ),
        (
            _("Statystyki"),
            {
                "fields": ("reading_time", "view_count"),
            },
        ),
    )

    # --- Akcje administracyjne ---

    # Dodaje akcje, które można wykonać na wielu zaznaczonych obiektach na liście
    actions = ["make_published", "make_draft", "make_archived"]

    @admin.action(description=_('Zmień status zaznaczonych na "Opublikowany"'))
    def make_published(self, request, queryset):
        """make_published"""
        queryset.update(status=BlogPost.Status.PUBLISHED)

    @admin.action(description=_('Zmień status zaznaczonych na "Szkic"'))
    def make_draft(self, request, queryset):
        """make_draft"""
        queryset.update(status=BlogPost.Status.DRAFT)

    @admin.action(description=_('Zmień status zaznaczonych na "Zarchiwizowany"'))
    def make_archived(self, request, queryset):
        """make_archived"""
        queryset.update(status=BlogPost.Status.ARCHIVED)
