from django.urls import path

from core.views.terms_and_conditions import (
    cookies_policy,
    privacy_policy,
    terms_and_conditions_webinars,
)

urlpatterns = [
    path(
        "regulamin-szkolen/",
        terms_and_conditions_webinars,
        name="terms_and_conditions_webinars",
    ),
    path(
        "polityka-prywatnosci/",
        privacy_policy,
        name="privacy_policy",
    ),
    path(
        "polityka-cookies/",
        cookies_policy,
        name="cookies_policy",
    ),
]
