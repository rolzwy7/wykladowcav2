from django.forms import CharField, Form

from core.forms.widgets import CheckboxWidget


class CrmAreYouSureForm(Form):
    """Form for confirming operations"""

    i_am_sure = CharField(
        widget=CheckboxWidget(attrs={"label": "Chcę wykonać tę operację"})
    )
