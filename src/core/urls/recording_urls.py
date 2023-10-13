from django.urls import path

from core.views.recording import recording_streaming, recording_token_page

urlpatterns = [
    path(
        "obejrzyj/<uuid:uuid>/",
        recording_token_page,
        name="recording_token_page",
    ),
    path(
        "stream/<uuid:uuid>/",
        recording_streaming,
        name="recording_streaming",
    ),
]
