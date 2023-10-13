from django.urls import path

from core.views.register_page import (
    register_activation_page,
    register_info_page,
    register_page,
)

urlpatterns = [
    path(
        "aktywacja/<uuid:activation_token>/",
        register_activation_page,
        name="register_activation_page",
    ),
    path("informacja/", register_info_page, name="register_info_page"),
    path("", register_page, name="register_page"),
]
