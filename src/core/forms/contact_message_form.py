from django.forms import EmailInput, HiddenInput, ModelForm, Textarea, TextInput

from core.models import ContactMessage


class ContactMessageForm(ModelForm):
    """Form for contact message"""

    class Meta:
        model = ContactMessage
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "message",
            "related_to",
        ]
        widgets = {
            "first_name": TextInput(attrs={"class": "form-control"}),
            "last_name": TextInput(attrs={"class": "form-control"}),
            "email": EmailInput(attrs={"class": "form-control"}),
            "phone_number": TextInput(attrs={"class": "form-control"}),
            "message": Textarea(attrs={"class": "form-control"}),
            "related_to": HiddenInput(attrs={"class": "form-control"}),
        }
