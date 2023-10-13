from django.forms import ModelForm

from core.forms.widgets import NumberFloatingInputWidget
from core.models import WebinarMetadata


class CrmLecturerPriceCardForm(ModelForm):
    """Type form for webinar application"""

    class Meta:
        model = WebinarMetadata
        fields = ["lecturer_price_netto"]
        widgets = {
            "lecturer_price_netto": NumberFloatingInputWidget(
                attrs={"label": "Cena NETTO wykładowcy"}
            )
        }
