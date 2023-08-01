from django.urls import path

from core.views.loyalty_program import (
    loyalty_program_page,
    loyalty_program_terms_of_service_accept_page,
)

urlpatterns = [
    path(
        "akceptacja-regulaminu/",
        loyalty_program_terms_of_service_accept_page,
        name="loyalty_program_terms_of_service_accept_page",
    ),
    path(
        "",
        loyalty_program_page,
        name="loyalty_program_page",
    ),
]
