from django.urls import path

from core.views.forgot_password_page import (
    ForgotPasswordCompletePage,
    ForgotPasswordConfirmPage,
    ForgotPasswordDonePage,
    ForgotPasswordPage,
)

urlpatterns = [
    path(
        "resetuj-haslo/<uidb64>/<token>/",
        ForgotPasswordConfirmPage.as_view(),
        name="forgot_password_confirm_page",
    ),
    path(
        "zmieniono-haslo/",
        ForgotPasswordCompletePage.as_view(),
        name="forgot_password_complete_page",
    ),
    path(
        "wyslano/",
        ForgotPasswordDonePage.as_view(),
        name="forgot_password_done_page",
    ),
    path(
        "",
        ForgotPasswordPage.as_view(),
        name="forgot_password_page",
    ),
]
