"""CRM Password Reset"""

# flake8: noqa=E501

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from core.models import User


def crm_user_password_reset(request, pk):
    """crm_user_password_reset"""
    try:
        # Fetch the user by ID
        user = User.objects.get(pk=pk)

        # Generate token
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)

        # Encode user ID
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Construct the password reset URL
        reset_path = reverse(
            "core:forgot_password_confirm_page", kwargs={"uidb64": uid, "token": token}
        )
        reset_url = f"{settings.BASE_URL}{reset_path}"

        template_name = "core/pages/crm/CrmUserPasswordResetPage.html"
        return TemplateResponse(
            request, template_name, {"reset_url": reset_url, "user": user}
        )

    except User.DoesNotExist:  # pylint: disable=no-member
        return HttpResponse("User not found", status=404)
