"""Blog list page"""

# flake8: noqa=E501

from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import BlogPost, WebinarAggregate, WebinarCategory


def blog_list_page(request, slug: str = ""):
    """blog_list_page"""

    context = {}

    if slug:
        # Pobierz obiekt kategorii lub zwróć błąd 404, jeśli nie istnieje.
        category = get_object_or_404(
            WebinarCategory.manager.get_blog_categories(), slug=slug
        )
        context["category"] = category
        filter_slugs = [slug]

        # Pobierz related webinars po kategorii
        related_aggregates: list[WebinarAggregate] = [
            _
            for _ in WebinarAggregate.manager.get_active_aggregates_for_category_slugs(
                filter_slugs
            )
        ]
        context["related_aggregates"] = related_aggregates
        context["related_aggregates_title"] = "Powiązane szkolenia"
    else:
        all_blog_categories = WebinarCategory.manager.get_blog_categories()
        filter_slugs = [str(_.slug) for _ in all_blog_categories]

        # Pobierz najblizsze related webinars top 10
        related_aggregates: list[WebinarAggregate] = [
            _ for _ in WebinarAggregate.manager.get_active_aggregates()[:10]
        ]
        context["related_aggregates"] = related_aggregates
        context["related_aggregates_title"] = "Najbliższe szkolenia"

    # Użyj managera BlogPost do pobrania opublikowanych artykułów
    # dla danej kategorii. Metoda `with_related_data` optymalizuje zapytanie.
    blog_posts = BlogPost.manager.get_blog_posts_for_category_slugs(filter_slugs)
    blog_posts_list = [_ for _ in blog_posts]

    if blog_posts_list:
        hero_article = blog_posts_list[0]
        articles = blog_posts_list[1:]
    else:
        hero_article = None
        articles = []

    # Przygotuj kontekst do przekazania do szablonu.
    context = {**context, "hero_article": hero_article, "articles": articles}

    # Zwróć TemplateResponse z odpowiednim szablonem i kontekstem.
    return TemplateResponse(
        request,
        "geeks/pages/blog/BlogList.html",
        context,
    )
