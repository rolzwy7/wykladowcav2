from django.urls import path

from core.views import (
    webinar_all_categories_page,
    webinar_category_lecturer_page,
    webinar_category_opinions_page,
    webinar_category_page,
    webinar_category_who_are_we_page,
)

urlpatterns = [
    path(
        "wszystkie/",
        webinar_all_categories_page,
        name="webinar_all_categries_page",
    ),
    path(
        "<slug:slug>/",
        webinar_category_page,
        name="webinar_category_page",
    ),
    path(
        "<slug:slug>/kim-jestesmy/",
        webinar_category_who_are_we_page,
        name="webinar_category_who_are_we_page",
    ),
    path(
        "<slug:slug>/wykladowcy/",
        webinar_category_lecturer_page,
        name="webinar_category_lecturer_page",
    ),
    path(
        "<slug:slug>/opinie/",
        webinar_category_opinions_page,
        name="webinar_category_opinions_page",
    ),
]
