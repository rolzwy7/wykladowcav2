from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import reverse_lazy


class ForgotPasswordPage(PasswordResetView):
    """Form for e-mail address and reset link sending"""

    template_name = "geeks/pages/forgot_password/password_reset_form.html"
    success_url = reverse_lazy("core:forgot_password_done_page")
    email_template_name = (
        "geeks/pages/forgot_password/password_reset_email.html"
    )


class ForgotPasswordDonePage(PasswordResetDoneView):
    """Done page for `ForgotPasswordPage`"""

    template_name = "geeks/pages/forgot_password/password_reset_done.html"


class ForgotPasswordConfirmPage(PasswordResetConfirmView):
    """Form for password reset (provide password two times)"""

    template_name = "geeks/pages/forgot_password/password_reset_confirm.html"
    success_url = reverse_lazy("core:forgot_password_complete_page")


class ForgotPasswordCompletePage(PasswordResetCompleteView):
    """Password reset completed"""

    template_name = "geeks/pages/forgot_password/password_reset_complete.html"
