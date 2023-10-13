from django.forms import CharField, EmailField, Form, PasswordInput


class LoginForm(Form):
    """Login form"""

    username = EmailField()
    password = CharField(widget=PasswordInput)
