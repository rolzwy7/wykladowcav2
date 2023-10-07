from django.forms import EmailField, Form


class ResignationForm(Form):
    """Form for adding resignation (e-mail) manually"""

    email = EmailField()
