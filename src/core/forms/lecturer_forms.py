from django.forms import ModelForm

from core.forms.widgets import (
    RatingWidget,
    TextareaFloatingInputWidget,
    TextFloatingInputWidget,
)
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
            "fullname": TextFloatingInputWidget(
                attrs={"label": "Imię i Nazwisko"}
            ),
            "company_name": TextFloatingInputWidget(
                attrs={"label": "Nazwa Firmy (opcjonalnie)"}
            ),
            "job_title": TextFloatingInputWidget(
                attrs={"label": "Stanowisko (opcjonalnie)"}
            ),
            "opinion_text": TextareaFloatingInputWidget(
                attrs={"label": "Treść opinii"}
            ),
            "rating": RatingWidget(),
        }
