"""Blog list page"""

# flake8: noqa=E501

from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.libs.blog.blog_advert import get_blogpost_advert_img_tag
from core.models import BlogPost, WebinarAggregate, WebinarCategory


def blog_list_page(request, slug: str):
    """
    Wyświetla listę artykułów blogowych dla danej kategorii.

    Pobiera obiekt kategorii na podstawie podanego sluga. Jeśli kategoria
    nie istnieje, zwraca błąd 404. Następnie, przy użyciu dedykowanego
    managera modelu BlogPost, pobiera wszystkie opublikowane artykuły
    przypisane do tej kategorii. Zapytanie jest zoptymalizowane pod kątem
    wydajności przez pobranie powiązanych danych (autor, kategorie)
    w jednym zapytaniu.
    """
    # Pobierz obiekt kategorii lub zwróć błąd 404, jeśli nie istnieje.
    category = get_object_or_404(WebinarCategory, slug=slug)

    # Użyj managera BlogPost do pobrania opublikowanych artykułów
    # dla danej kategorii. Metoda `with_related_data` optymalizuje zapytanie.
    articles = BlogPost.manager.get_blog_posts_for_category_slugs([slug])

    # Przygotuj kontekst do przekazania do szablonu.
    context = {
        "category": category,
        "articles": articles,
    }

    # Zwróć TemplateResponse z odpowiednim szablonem i kontekstem.
    return TemplateResponse(
        request,
        "geeks/pages/blog/BlogList.html",
        context,
    )
