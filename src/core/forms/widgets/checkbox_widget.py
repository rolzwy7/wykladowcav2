from django.forms.widgets import CheckboxInput


class CheckboxWidget(CheckboxInput):
    input_type = "checkbox"
    template_name = "core/widgets/checkbox.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        return context
