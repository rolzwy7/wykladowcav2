from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import CharField, EmailField, Form

from core.forms.widgets import (
    EmailFloatingInputWidget,
    PasswordFloatingInputWidget,
    TextFloatingInputWidget,
)
from core.models import User


class RegistrationForm(Form):
    """Registration form"""

    first_name = CharField(
        widget=TextFloatingInputWidget(attrs={"label": "Imię"}),
        max_length=15,
        min_length=3,
    )
    last_name = CharField(
        widget=TextFloatingInputWidget(attrs={"label": "Nazwisko"}),
        max_length=25,
        min_length=3,
    )

    email = EmailField(
        widget=EmailFloatingInputWidget(
            attrs={
                "label": "E-mail",
                "properties": [("autocomplete", '"username"')],
            }
        )
    )

    password1 = CharField(
        max_length=64,
        widget=PasswordFloatingInputWidget(
            attrs={
                "label": "Hasło",
                "properties": [("autocomplete", '"new-password"')],
            }
        ),
    )
    password2 = CharField(
        max_length=64,
        widget=PasswordFloatingInputWidget(
            attrs={
                "label": "Powtórz hasło",
                "properties": [("autocomplete", '"new-password"')],
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data["password1"]
        password2 = cleaned_data["password2"]
        email = cleaned_data["email"]

        if password1 != password2:
            raise ValidationError("Hasła nie są takie same")

        if User.objects.filter(username=email).exists():
            raise ValidationError(
                "Użytkownik o takim adresie e-mail już istnieje."
            )

        validate_password(password1)
