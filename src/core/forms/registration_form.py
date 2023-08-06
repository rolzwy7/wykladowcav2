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
        max_length=150, widget=TextFloatingInputWidget(attrs={"label": "Imię"})
    )
    last_name = CharField(
        max_length=150,
        widget=TextFloatingInputWidget(attrs={"label": "Nazwisko"}),
    )

    email = EmailField(
        widget=EmailFloatingInputWidget(attrs={"label": "E-mail"})
    )

    password1 = CharField(
        max_length=64,
        widget=PasswordFloatingInputWidget(attrs={"label": "Hasło"}),
    )
    password2 = CharField(
        max_length=64,
        widget=PasswordFloatingInputWidget(attrs={"label": "Powtórz hasło"}),
    )

    # def clean_password1(self): TODO
    #     """Clean password1 field"""
    #     password1 = self.cleaned_data["password1"]
    #     password2 = self.cleaned_data["password2"]
    #     if password1 != password2:
    #         raise ValidationError("Hasła nie są takie same")
    #     validate_password(password1)
    #     return password1

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
