# flake8: noqa=E501

from django.urls import path

from core.views.blog import blog_article_page

urlpatterns = [
    path(
        "<slug:slug>/",
        blog_article_page,
        name="blog_article_page",
    ),
]
