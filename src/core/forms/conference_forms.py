"""Conference forms"""

from django.forms import CheckboxInput, ModelForm, Select, TextInput

from core.models import ConferenceFreeParticipant


class ConferenceFreeParticipantModelForm(ModelForm):
    """ConferenceFreeParticipantModelForm"""

    class Meta:
        """meta"""

        model = ConferenceFreeParticipant
        fields = [
            "first_name",
            "last_name",
            "voivodeship",
            "phone",
            "email",
            "know_from",
            "using_closed_webinars",
            "consent",
        ]

        widgets = {
            "first_name": TextInput(attrs={"class": "form-control"}),
            "last_name": TextInput(attrs={"class": "form-control"}),
            "voivodeship": Select(attrs={"class": "form-control"}),
            "phone": TextInput(attrs={"class": "form-control"}),
            "email": TextInput(attrs={"class": "form-control"}),
            "know_from": Select(attrs={"class": "form-control"}),
            "using_closed_webinars": Select(attrs={"class": "form-control"}),
            "consent": CheckboxInput(attrs={"class": "form-check-input"}),
        }
