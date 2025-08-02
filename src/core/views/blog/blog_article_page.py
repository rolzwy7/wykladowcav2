"""BlogPost View"""

# flake8: noqa=E501

from django.db.models import F
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import BlogPost


def blog_article_page(request, slug: str):
    """
    Wyświetla stronę pojedynczego artykułu blogowego.

    Pobiera tylko opublikowane artykuły i zwraca błąd 404, jeśli
    artykuł nie istnieje, jest szkicem lub jego data publikacji
    jeszcze nie nadeszła.

    Po pomyślnym pobraniu artykułu, zwiększa jego licznik wyświetleń.
    """
    template_name = "geeks/pages/blog/BlogArticle.html"

    # Użyj get_object_or_404, aby elegancko obsłużyć przypadek,
    # gdy obiekt nie zostanie znaleziony.
    #
    # Wykorzystaj stworzony wcześniej manager i jego metody, aby kod był czysty
    # i zgodny z logiką biznesową zdefiniowaną w modelu.
    # Metoda `published()` filtruje status i datę publikacji.
    # Metoda `with_related_data()` optymalizuje zapytanie (prefetch/select_related).
    article = get_object_or_404(
        BlogPost.manager.published().with_related_data(), slug=slug
    )

    # Zwiększ licznik wyświetleń. Użycie F() pozwala uniknąć tzw. "race condition".
    # Django wykona operację dodawania bezpośrednio w bazie danych.
    # Używamy .filter(pk=...).update(...) zamiast article.save(),
    # aby uniknąć ponownego wywołania sygnałów save().
    if not request.user.is_staff:
        BlogPost.manager.filter(pk=article.pk).update(view_count=F("view_count") + 1)

    return TemplateResponse(
        request,
        template_name,
        {
            "article": article,
        },
    )
