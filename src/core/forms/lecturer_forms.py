from django.forms import ModelForm, Select, Textarea, TextInput

from core.models import LecturerOpinion


class LecturerOpinionForm(ModelForm):
    """Form for adding lecturer opinion"""

    class Meta:
        model = LecturerOpinion
        fields = [
            "fullname",
            "company_name",
            "job_title",
            "opinion_text",
            "rating",
        ]
        widgets = {
            "fullname": TextInput(attrs={"class": "form-control"}),
            "company_name": TextInput(attrs={"class": "form-control"}),
            "job_title": TextInput(attrs={"class": "form-control"}),
            "opinion_text": Textarea(attrs={"class": "form-control"}),
            "rating": Select(attrs={"class": "form-control"}),
        }
