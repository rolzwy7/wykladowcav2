from django.urls import path

from core.views.crm.lecturer import (
    lecturer_add_opinions_page,
    lecturer_list_page,
    lecturer_stats_page,
)

urlpatterns = [
    path(
        "<int:pk>/dodaj-opinie/",
        lecturer_add_opinions_page,
        name="lecturer_add_opinions_page",
    ),
    path(
        "<int:pk>/",
        lecturer_stats_page,
        name="lecturer_stats_page",
    ),
    path(
        "",
        lecturer_list_page,
        name="lecturer_list_page",
    ),
]
