# flake8: noqa=E501

from django.urls import path

from core.views.blog import blog_article_page, blog_list_page

urlpatterns = [
    path(
        "kategoria/<slug:slug>/",
        blog_list_page,
        name="blog_list_page",
    ),
    path(
        "<slug:slug>/",
        blog_article_page,
        name="blog_article_page",
    ),
    path(
        "",
        blog_list_page,
        name="blog_list_page",
    ),
]
