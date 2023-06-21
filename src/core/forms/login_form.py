from django.forms import CharField, EmailField, Form, PasswordInput


class LoginForm(Form):
    username = EmailField()
    password = CharField(widget=PasswordInput)
