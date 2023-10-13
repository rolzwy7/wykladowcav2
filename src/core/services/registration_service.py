from random import choice

from django.conf import settings

from core.libs.notifications.email import EmailMessage, EmailTemplate
from core.models import User

COMPANY_NAME = settings.COMPANY_NAME


class RegistrationService:
    """Registration service"""

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.email = username
        self.password = password

    @staticmethod
    def activate_user_by_activation_token(activation_token: str):
        """Activate user by activation token"""
        user: User = User.objects.get(activation_token=activation_token)
        user.is_active = True
        user.save()
        return user

    @staticmethod
    def get_user_by_activation_token(activation_token: str):
        """Activate user by activation token"""
        user: User = User.objects.get(activation_token=activation_token)
        return user

    def create_user(self, first_name: str, last_name: str) -> User:
        """Create user"""
        user: User = User.objects.create_user(
            self.username, email=self.email, password=self.password
        )
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = False
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user

    def send_confirmation_email(self, activation_token: str):
        """Send registration confirmation e-mail"""
        template_name = "email/EmailRegistration.html"
        email_template = EmailTemplate(
            template_name,
            {
                "activation_token": activation_token,
            },
        )
        email_message = EmailMessage(
            email_template,
            choice(
                [
                    f"Stworzyłeś konto w serwisie {COMPANY_NAME}",
                    f"Utworzyłeś konto w serwisie {COMPANY_NAME}",
                    f"Utworzono konto w serwisie {COMPANY_NAME}",
                    f"Rejestracja konta w serwisie {COMPANY_NAME}",
                ]
            ),
            self.email,
        )
        email_message.send()
