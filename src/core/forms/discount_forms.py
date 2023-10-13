from django.forms import CharField, Form

from core.forms.widgets import TextFloatingInputWidget


class DiscountCodeForm(Form):
    """Discount code form"""

    discount_code = CharField(
        widget=TextFloatingInputWidget(attrs={"label": "Wpisz kod promocyjny"})
    )
