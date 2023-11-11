from django.urls import path

from core.views.user_account import my_recordings_page

urlpatterns = [
    path(
        "nagrania/",
        my_recordings_page,
        name="my_recordings_page",
    )
]
