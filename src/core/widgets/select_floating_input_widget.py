from django.forms.widgets import Select


class SelectFloatingInputWidget(Select):
    input_type = "select"
    template_name = "core/widgets/select_floating_input.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        return context
