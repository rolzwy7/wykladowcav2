from django.forms import CharField, DateTimeField, Form

from core.forms.widgets import CheckboxWidget, DatepickerWidget


class CrmMoveActionForm(Form):
    """Type form for webinar application"""

    new_date = DateTimeField(
        input_formats=["%d.%m.%Y, %H:%M"], widget=DatepickerWidget()
    )

    i_am_sure = CharField(
        widget=CheckboxWidget(attrs={"label": "Chcę wykonać tę operację"})
    )
