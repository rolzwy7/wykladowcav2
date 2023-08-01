from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import CharField, EmailField, Form, PasswordInput


class RegistrationForm(Form):
    """Registration form"""

    first_name = CharField(max_length=150)
    last_name = CharField(max_length=150)

    email = EmailField()

    password1 = CharField(widget=PasswordInput)
    password2 = CharField(widget=PasswordInput)

    # def clean_password1(self): # TODO:
    #     password1 = self.cleaned_data["password1"]
    #     validate_password(password1)
    #     return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data["password1"]
        password2 = cleaned_data["password2"]
        if password1 != password2:
            raise ValidationError("Hasła nie są takie same")
