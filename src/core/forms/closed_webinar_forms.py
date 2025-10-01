"""Closed webinars forms"""

# flake8: noqa=E501

from django import forms

from core.models import ClosedWebinarContactMessage


class ClosedWebinarContactForm(forms.ModelForm):
    class Meta:
        model = ClosedWebinarContactMessage
        fields = [
            "full_name",
            "company",
            "number_of_participants",
            "phone",
            "email",
            "message",
        ]
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Imię i nazwisko"}
            ),
            "company": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Firma (opcjonalne)"}
            ),
            "number_of_participants": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Potencjalna liczba osób do przeszkolenia",
                }
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Telefon (opcjonalne)"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Adres E-mail"}
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Jakiej tematyki ma dotyczyć szkolenie? Jakie są Państwa oczekiwania?",
                    "rows": 5,
                    "maxlength": "1000",
                }
            ),
        }
        labels = {
            "full_name": "Imię i nazwisko *",
            "company": "Firma",
            "phone": "Telefon",
            "email": "Email *",
            "message": "Treść wiadomości *",
        }
