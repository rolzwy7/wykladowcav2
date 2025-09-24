"""BlogPost View"""

# flake8: noqa=E501

from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.libs.blog.blog_advert import get_blogpost_advert_img_tag
from core.libs.spy import create_spy_object
from core.models import BlogPost, BlogView, WebinarAggregate


def blog_article_page(request, slug: str):
    """
    Wyświetla stronę pojedynczego artykułu blogowego.

    Pobiera tylko opublikowane artykuły i zwraca błąd 404, jeśli
    artykuł nie istnieje, jest szkicem lub jego data publikacji
    jeszcze nie nadeszła.

    Po pomyślnym pobraniu artykułu, zwiększa jego licznik wyświetleń.
    """

    # Użyj get_object_or_404, aby elegancko obsłużyć przypadek,
    # gdy obiekt nie zostanie znaleziony.
    #
    # Wykorzystaj stworzony wcześniej manager i jego metody, aby kod był czysty
    # i zgodny z logiką biznesową zdefiniowaną w modelu.
    # Metoda `published()` filtruje status i datę publikacji.
    # Metoda `with_related_data()` optymalizuje zapytanie (prefetch/select_related).
    article: BlogPost = get_object_or_404(
        BlogPost.manager.published().with_related_data(), slug=slug
    )

    # Zwiększ licznik wyświetleń. Użycie F() pozwala uniknąć tzw. "race condition".
    # Django wykona operację dodawania bezpośrednio w bazie danych.
    # Używamy .filter(pk=...).update(...) zamiast article.save(),
    # aby uniknąć ponownego wywołania sygnałów save().
    if not request.user.is_staff:
        BlogPost.manager.filter(pk=article.pk).update(view_count=F("view_count") + 1)
        with transaction.atomic():
            spy_object = create_spy_object(request, "BLOG_ARTICLE_VIEW")
            blog_view = BlogView(blog_post=article, spy_object=spy_object)
            blog_view.save()

    related_aggregates: list[WebinarAggregate] = []
    if article.show_related_webinars:
        for _ in WebinarAggregate.manager.get_active_aggregates_for_category_slugs(
            [cat.slug for cat in article.categories.all()]
        ):
            related_aggregates.append(_)

    # Article content
    article_content = article.content

    # Advert aggregate
    if article.advert_aggregate and article.advert_aggregate.has_active_webinars:
        # Ustawiony jest agregat i ma terminy
        advert_aggregate = article.advert_aggregate
        advert_img_tag = get_blogpost_advert_img_tag(advert_aggregate)
        article_content = article_content.replace("[[ADVERT_BLOGPOST]]", advert_img_tag)
    elif len(related_aggregates) != 0:
        # Wez z powiazanych szkolen
        _counter = 0
        while "[[ADVERT_BLOGPOST]]" in article_content:
            advert_aggregate = related_aggregates[_counter % len(related_aggregates)]
            _counter += 1
            advert_img_tag = get_blogpost_advert_img_tag(advert_aggregate)
            article_content = article_content.replace(
                "[[ADVERT_BLOGPOST]]", advert_img_tag, 1
            )
    else:
        # Jak nie ma to wyrzuc reklamy
        article_content = article_content.replace("[[ADVERT_BLOGPOST]]", "")

    return TemplateResponse(
        request,
        "geeks/pages/blog/BlogArticle.html",
        {
            "article": article,
            "article_content": article_content,
            "related_aggregates": related_aggregates,
        },
    )
