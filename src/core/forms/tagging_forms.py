from django.forms import FileField, Form


class TaggingAddEmailsForm(Form):
    """Form for adding emails to tagging"""

    file = FileField()
