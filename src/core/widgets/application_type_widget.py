from django.forms.widgets import Select
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class ApplicationTypeWidget(Select):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        return mark_safe(
            render_to_string(
                "widgets/ApplicationTypeWidget.html",
                {
                    "name": name,
                    "choices": self.choices,
                },
            )
        )
