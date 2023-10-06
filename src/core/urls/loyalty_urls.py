from django.urls import path

from core.views.loyalty_program import (
    loyalty_program_page,
    loyalty_program_terms_of_service_accept_page,
)
from core.views.loyalty_program_info_page import (
    loyalty_program_info_page,
    loyalty_program_video_page,
)

urlpatterns = [
    path(
        "akceptacja-regulaminu/",
        loyalty_program_terms_of_service_accept_page,
        name="loyalty_program_terms_of_service_accept_page",
    ),
    path(
        "informacje/",
        loyalty_program_info_page,
        name="loyalty_program_info_page",
    ),
    path(
        "wideo-prezentacja/",
        loyalty_program_video_page,
        name="loyalty_program_video_page",
    ),
    path(
        "",
        loyalty_program_page,
        name="loyalty_program_page",
    ),
]
